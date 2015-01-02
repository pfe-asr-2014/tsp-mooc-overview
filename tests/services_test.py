import unittest, mock, yaml, docker
from overview.services import Services
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


class ServicesMiscTest(unittest.TestCase):
    def setUp(self):
        self.docker = mock.create_autospec(docker.Client)
        self.services = Services(self.docker, "tests/config.yml")

    def test_by_id(self):
        self.assertEqual(self.services.by_id('django-example'),
            self.services.cfg['services'][1])

        self.assertEqual(self.services.by_id('schmilblick'), None)

        self.assertEqual(self.services.by_id('tsp-mooc-overview'),
            self.services.cfg['services'][0])

    def test_docker_state(self):
        self.docker.images.return_value = 'images'
        self.docker.containers.return_value = 'containers'

        self.assertEqual(self.services.docker_state(),
            {'images': 'images', 'containers': 'containers'})

        self.docker.images.assert_called_with(name = '*tsp*')
        self.assertTrue(self.docker.containers.called)


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

    @mock.patch.object(Services, 'uninstall')
    @mock.patch.object(Services, 'install')
    @mock.patch.object(Services, 'stop')
    @mock.patch.object(Services, 'run')
    @mock.patch.object(Services, 'by_id')
    @mock.patch.object(Services, 'state')
    def test_change_state(self, state, by_id,
                          mock_run, mock_stop, mock_install, mock_uninstall):
        service = {}
        by_id.return_value = service

        # The desired state is the current state
        state.return_value = self.services.STATE_RUNNING
        self.assertEqual(
            'service is already in the given state (running)',
            self.services.change('service', self.services.STATE_RUNNING)
        )

        # Unknown state
        self.assertEqual(
            'The given state (helloWorld) is incorrect.',
            self.services.change('service', 'helloWorld')
        )

        # Run the service
        state.return_value = self.services.STATE_STOPPED
        self.services.change('service', self.services.STATE_RUNNING)
        mock_run.assert_called_with(service)

        # Stop the service
        state.return_value = self.services.STATE_RUNNING
        self.services.change('service', self.services.STATE_STOPPED)
        mock_stop.assert_called_with(service)

        # Install the service
        state.return_value = self.services.STATE_NOT_INSTALLED
        self.services.change('service', self.services.STATE_STOPPED)
        mock_install.assert_called_with(service)

        # Uninstall the service
        state.return_value = self.services.STATE_STOPPED
        self.services.change('service', self.services.STATE_NOT_INSTALLED)
        mock_uninstall.assert_called_with(service)

    @mock.patch.object(Services, 'state')
    def test_get_states(self, state):
        state.return_value = 'State'

        self.assertEqual(self.services.states(),
            {'services': [
                {
                'completeName': 'TSP MOOC Overview',
                'state': 'State',
                'id': 'tsp-mooc-overview'
                },
                {
                'completeName': 'Django overview',
                'state': 'State',
                'id': 'django-example'
                }
            ]})
        self.assertEqual(state.call_args_list, [
            call(self.services.cfg['services'][0]),
            call(self.services.cfg['services'][1])
            ])


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
