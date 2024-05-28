import pytest
from cases.base_case import BaseCase
from pages.template.template import Template
from utils import load_yaml


class TestTemplate(BaseCase):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.template = Template(cls.driver)

    @pytest.mark.hot
    @pytest.mark.parametrize('kwargs', load_yaml("./data/template/template.yaml"))
    def test_01_search(self, kwargs):
        self.template.run(**kwargs)
