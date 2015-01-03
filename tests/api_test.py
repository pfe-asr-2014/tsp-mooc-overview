import overview, unittest, mock, json
from overview.services import Services


class ApiV1Test(unittest.TestCase):
    def send_patch_json(self, url, json_data):
        return self.app.patch(url,
                data = json.dumps(json_data),
                headers = [('Content-Type', 'application/json')])

    def setUp(self):
        self.app = overview.app.test_client()

    @mock.patch.object(Services, 'docker_state')
    def test_get_docker_state(self, mock_docker_state):
        mock_docker_state.return_value = {'message':'docker_state_by_services'}
        rv = self.app.get('/api/v1/docker')
        self.assertEqual(rv.data, '{\n  "message": "docker_state_by_services"\n}')

    @mock.patch.object(Services, 'states')
    def test_get_services_state(self, mock_services_state):
        mock_services_state.return_value = {'message':'services_state'}
        rv = self.app.get('/api/v1/services')
        self.assertEqual(rv.data, '{\n  "message": "services_state"\n}')

    @mock.patch.object(Services, 'change')
    def test_patch_service_state(self, mock_services_change):

        # When the change is valid (from services.change perspective)
        mock_services_change.return_value = None
        rv = self.send_patch_json('/api/v1/services/serviceId',
                { 'state': Services.STATE_RUNNING })

        self.assertEqual(rv.data,
            '{\n  "message": "Correctly applied. Change in progress."\n}')

        # Verify that the change has been given
        mock_services_change.assert_called_with('serviceId', Services.STATE_RUNNING)

        # When the change is invalid (from services.change perspective)
        mock_services_change.return_value = 'error description'
        rv = self.send_patch_json('/api/v1/services/serviceId',
                { 'state': Services.STATE_RUNNING })

        self.assertEqual(rv.data,
            '{\n  "error": "error description", \n'
            '  "message": "This change cannot be made"\n}')
