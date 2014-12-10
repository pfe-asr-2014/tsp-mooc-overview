import unittest, mock, yaml
from services import Services
from docker import Client
from mock import call

class ServicesTest(unittest.TestCase):
    def setUp(self):
        self.docker = mock.create_autospec(Client)
        self.services = Services(self.docker, "config_test.yml")

    def test_create_instance_without_config(self):
        services = Services(self.docker)

        # By default no config is loaded
        self.assertEqual(services.cfg, {'services': []})

    def test_create_instance_with_config(self):
        services = Services(self.docker, "config_test.yml")
        with open("config_test.yml", 'r') as ymlfile:
            config = yaml.load(ymlfile)

        # Assert the config is as loaded in config_test.yml
        self.assertEqual(services.cfg, config)

    def test_provide_service_states_as_constant(self):
        self.assertIsNotNone(self.services.STATE_INSTALLING)
        self.assertIsNotNone(self.services.STATE_UNINSTALLING)
        self.assertIsNotNone(self.services.STATE_STOPPING)

        self.assertIsNotNone(self.services.STATE_RUNNING)
        self.assertIsNotNone(self.services.STATE_STOPPED)
        self.assertIsNotNone(self.services.STATE_NOT_INSTALLED)

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

    def test_install_service(self):
        service = self.services.cfg['services'][1]
        stack = service['stack']

        self.services.install(service)

        self.assertEqual(self.docker.create_container.call_args_list, [
            call(
                name = stack[0]['containerName'],
                image = stack[0]['image'],
                environment = stack[0]['environment'],
                ports = None,
                volumes = None
            ),
            call(
                name = stack[1]['containerName'],
                image = stack[1]['image'],
                environment = None,
                ports = stack[1]['ports'],
                volumes = stack[1]['volumes']
            )
        ])

    def test_uninstall_service(self):
        return
        service = self.services.cfg['services'][1]
        stack = service['stack']

        self.assertEqual(self.docker.remove_image.call_args_list, [
            call(name = stack[0]['image']),
            call(name = stack[1]['image'])
        ])

    def test_run_service(self):
        # Here we verify the links are made
        pass

    def test_stop_service(self):
        pass

if __name__ == '__main__':
    unittest.main()
