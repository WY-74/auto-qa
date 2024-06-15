from config.chrome_options import get_driver
from config.credentials import credentials
from utils.parse_yaml import load_yaml


class BaseCase:
    @classmethod
    def setup_class(cls):
        cls.credentials = credentials
        cls.driver = get_driver()
        cls.locators = cls.get_locators()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    @classmethod
    def get_locators(cls):
        module = cls.__module__.replace("test_", "")
        return load_yaml(f"./locators/{module}/{module}.yaml")
