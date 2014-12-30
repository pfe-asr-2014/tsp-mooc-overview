import unittest, mock, yaml, docker
from services import Services
from mock import call

class ServicesConfigTest(unittest.TestCase):
    def setUp(self):
        self.docker = mock.create_autospec(docker.Client)

    def test_create_instance_without_config(self):
        services = Services(self.docker)

        # By default no config is loaded
        self.assertEqual(services.cfg, {'services': []})

    def test_create_instance_with_config(self):
        services = Services(self.docker, "tests/config.yml")
        with open("tests/config.yml", 'r') as ymlfile:
            config = yaml.load(ymlfile)

        # Assert the config is as loaded in config_test.yml
        self.assertEqual(services.cfg, config)

    def test_provide_service_states_as_constant(self):
        services = Services(self.docker, "tests/config.yml")

        self.assertIsNotNone(services.STATE_INSTALLING)
        self.assertIsNotNone(services.STATE_UNINSTALLING)
        self.assertIsNotNone(services.STATE_STOPPING)

        self.assertIsNotNone(services.STATE_RUNNING)
        self.assertIsNotNone(services.STATE_STOPPED)
        self.assertIsNotNone(services.STATE_NOT_INSTALLED)


class ServicesStateTest(unittest.TestCase):
    def setUp(self):
        self.docker = mock.create_autospec(docker.Client)
        self.services = Services(self.docker, "tests/config.yml")

    def test_get_state_not_installed(self):
        cfg = self.services.cfg['services'][1]

        self.docker.images.return_value = []
        self.docker.containers.return_value = [{'Image':None}]

        state = self.services.state(cfg)

        self.assertEqual(state, self.services.STATE_NOT_INSTALLED)

    def test_get_state_stopped(self):
        cfg = self.services.cfg['services'][1]

        self.docker.images.return_value = ['']
        self.docker.containers.return_value = [{'Image':None}]

        state = self.services.state(cfg)

        self.assertEqual(state, self.services.STATE_STOPPED)

    def test_get_state_running(self):
        cfg = self.services.cfg['services'][1]

        self.docker.images.return_value = ['']
        self.docker.containers.return_value = [
            {'Image':'paintedfox/postgresql'},
            {'Image':'djangodocker_web'}
        ]

        state = self.services.state(cfg)

        self.assertEqual(state, self.services.STATE_RUNNING)


class ServicesOperationTest(unittest.TestCase):
    def setUp(self):
        self.docker = mock.create_autospec(docker.Client)
        self.services = Services(self.docker, "tests/config.yml")

    def test_install_service(self):
        self.services.install(self.services.cfg['services'][1])

        self.assertEqual(self.docker.create_container.call_args_list, [
            call(
                name = 'db',
                image = 'paintedfox/postgresql',
                environment = {'USER':'docker', 'PASS':'docker', 'DB':'docker'},
                ports = None,
                volumes = None
            ),
            call(
                name = 'djangodocker_web',
                image = 'djangodocker_web',
                environment = None,
                ports = ['8080'],
                volumes = ['/app']
            )
        ])

    def test_uninstall_service(self):
        self.services.uninstall(self.services.cfg['services'][1])

        self.assertEqual(self.docker.remove_image.call_args_list, [
            call(image = 'paintedfox/postgresql'),
            call(image = 'djangodocker_web')
        ])

    def test_stop_service(self):
        self.services.stop(self.services.cfg['services'][1])

        self.assertEqual(self.docker.stop.call_args_list, [
            call(container = 'db'),
            call(container = 'djangodocker_web')
        ])

    def test_run_service(self):
        self.services.run(self.services.cfg['services'][1])

        self.assertEqual(self.docker.start.call_args_list, [
            call(
                container = 'db',
                links = None,
                port_bindings = None,
                binds = None
            ),
            call(
                container = 'djangodocker_web',
                links = [("db", "db")],
                port_bindings = {8080: 8000},
                binds = {'/app': {'bind': '/app'}}
            )
        ])
