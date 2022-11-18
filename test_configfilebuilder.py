import unittest
from src.configfile import ConfigFileGenerator


class TestConfigfile(unittest.TestCase):
    def setUp(self):
        self.test_path = "./test_results/test_config.ini"
        self.test_config = ConfigFileGenerator(self.test_path)
        self.configmap_type_OK = {
            "DEFAULT": {
                "eodhistoricaldata_api_key": "tbd1",
                "tiingo_dummy_api_key": "dummy1",
                "alphavantage_api_key": "dummy2",
                "iex_cloud_dummy_api_key": "dummy3",
                "iex_cloud_api_key": "dummy4",
            }
        }

        self.configmap_type_NOK_1 = {"key1": "10", "key2": 23}
        self.configmap_type_NOK_2 = ["key1", "key2"]

        self.other_configmap_type_OK = {
            "NEW_API_KEYS": {
                "eodhistoricaldata_api_key": "tbd1",
                "tiingo_dummy_api_key": "dummy1",
                "alphavantage_api_key": "dummy2",
                "iex_cloud_dummy_api_key": "dummy3",
                "iex_cloud_api_key": "dummy4",
            }
        }

    def test_write_config(self):
        self.test_config.write_config(self.configmap_type_OK)
        self.test_config.write_config(self.configmap_type_NOK_1)
        self.test_config.write_config(self.configmap_type_NOK_2)

    def test_write_config_raise_typeError_exception(self):
        pass

    def test_write_config_raise_configErr_exception(self):
        pass

    def test_add_config(self):
        self.test_config.add_config(self.other_configmap_type_OK)
        pass

    def test_add_config_raise_typeError_exception(self):
        self.test_config.add_config(self.other_configmap_type_OK)
        pass

    def test_add_config_raise_configErr_exception(self):
        self.test_config.add_config(self.other_configmap_type_OK)
        pass

    def test_update_section(self):
        pass

    def test_rm_section(self):
        pass


if "__name__" == "__main__":
    unittest.main()
