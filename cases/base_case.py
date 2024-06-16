from config.chrome_options import get_driver
from config.credentials import credentials
from base.api import ApiKeys
from utils.parse_yaml import load_yaml


class BaseCase:
    @classmethod
    def setup_class(cls):
        cls.credentials = credentials
        cls.module = cls.__module__
        cls.init()

    @classmethod
    def teardown_class(cls):
        if cls.module.split("_")[1] == "web":
            cls.driver.quit()

    @classmethod
    def get_locators(cls):
        _module = cls.module.split("_")[-1]
        return load_yaml(f"./locators/{_module}/{_module}.yaml")

    @classmethod
    def init(cls):
        if cls.module.split("_")[1] == "web":
            cls.driver = get_driver()
            cls.locators = cls.get_locators()
        elif cls.module.split("_")[1] == "api":
            cls.api = ApiKeys(cls.credentials["url"])
        else:
            raise Exception("module name must be: test_web/api_xxx")
