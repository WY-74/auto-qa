import pytest
from tests.base_case import BaseCase
from pages.login.login_pages import LoginPages
from utils import load_yaml, load_data_from_yaml, load_locators_from_yaml
from config.log import logger


class TestLogin(BaseCase):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.login = LoginPages(cls.driver)
        logger.info("setup_class finished")

    @pytest.mark.hot
    @pytest.mark.parametrize('kwargs', load_data_from_yaml("./cases/login/login.yaml"))
    def test_01_login(self, kwargs):
        locators = load_locators_from_yaml("./cases/login/login.yaml")
        self.login.run(locators=locators, **kwargs)
