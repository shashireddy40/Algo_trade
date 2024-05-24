import unittest
from unittest.mock import patch
import login

class TestLogin(unittest.TestCase):

    @patch('login.SmartConnect')
    @patch('login.helpers.load_config')
    def test_login(self, mock_load_config, mock_smart_connect):
        mock_load_config.return_value = {
            'api_keys': {
                'your_api_key': 'test_api_key',
                'userID': 'test_user',
                'pwd': 'test_pwd',
                'totp_key': 'test_totp_key'
            }
        }
        mock_smart_connect.return_value.generateSession.return_value = {
            'status': True,
            'data': {
                'jwtToken': 'test_jwt',
                'refreshToken': 'test_refresh'
            }
        }
        obj, authToken, refreshToken, feedToken, res = login.login('/path/to/config.yml')
        self.assertEqual(authToken, 'test_jwt')
        self.assertEqual(refreshToken, 'test_refresh')

if __name__ == '__main__':
    unittest.main()
