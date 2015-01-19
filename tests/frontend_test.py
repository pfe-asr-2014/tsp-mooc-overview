import mock, overview, os
from flask.ext.testing import TestCase
from overview.services import Services

class FrontendTest(TestCase):
    def create_app(self):
        return overview.app

    @mock.patch.object(Services, 'states')
    def test_home(self, mock_services_states):
        states = {}
        mock_services_states.return_value = states

        self.client.get('/')

        self.assert_template_used('index.html')
        self.assert_context('title', 'Overview')
        self.assert_context('state', states)

    def test_courses_url(self):
        # Without the env variable set, we default to localhost
        self.client.get('/')
        self.assert_context('base', 'localhost')

        # With the env var, we pass it to the template
        os.environ["HOST_IP"] = "192.168.10.10"
        self.client.get('/')
        self.assert_context('base', '192.168.10.10')
