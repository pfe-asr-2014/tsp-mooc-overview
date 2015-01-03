import unittest
from overview.helpers import service_state_toclass_filter

class FilterToClassTest(unittest.TestCase):

    def test_state_stopped(self):
        self.assertEqual('color-red', service_state_toclass_filter('Stopped'))

    def test_state_running(self):
        self.assertEqual('color-green', service_state_toclass_filter('Running'))

    def test_state_not_installed(self):
        self.assertEqual('color-gray', service_state_toclass_filter('Not Installed'))

    def test_state_unknown(self):
        self.assertEqual('', service_state_toclass_filter('Installing'))
        self.assertEqual('', service_state_toclass_filter('Uninstalling'))
        self.assertEqual('', service_state_toclass_filter('Stopping'))
        self.assertEqual('', service_state_toclass_filter('Whatever'))
