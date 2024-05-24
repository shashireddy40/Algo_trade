import unittest
import helpers

class TestHelpers(unittest.TestCase):

    def test_load_config(self):
        config = helpers.load_config('/path/to/config.yml')
        self.assertIn('api_keys', config)

    def test_fetch_instrument_list(self):
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        instrument_list = helpers.fetch_instrument_list(url)
        self.assertIsInstance(instrument_list, list)

if __name__ == '__main__':
    unittest.main()
