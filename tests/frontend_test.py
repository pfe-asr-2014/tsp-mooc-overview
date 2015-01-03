import mock, overview
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
