import pytest
from cases.base_case import BaseCase
from pages.template.template import Template
from utils.parse_yaml import load_yaml
from config.log import logger


class TestWebTemplate(BaseCase):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.template = Template(cls.driver)
        logger.info("setup_class finished")

    @pytest.mark.hot
    @pytest.mark.web
    @pytest.mark.parametrize('data', load_yaml("./data/web/template/template.yaml"))
    def test_01_search(self, data):
        self.template.run(self.locators, data)
