import pytest
from cases.base_case import BaseCase
from utils.parse_yaml import load_yaml


class TestApiTemplate(BaseCase):
    @pytest.mark.hot
    @pytest.mark.api
    @pytest.mark.parametrize('data', load_yaml("./data/api/template/template.yaml"))
    def test_01_search(self, data):
        response = self.api.get(path="s", params=data)
