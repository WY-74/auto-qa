from ddt import ddt, file_data
from cases.base_case import BaseCase


@ddt
class TestBaidu(BaseCase):
    @file_data("../../data/template/template.yaml")
    def test_01_search(self, **kwargs): ...
