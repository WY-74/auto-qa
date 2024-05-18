from ddt import ddt, file_data
from cases.base_case import BaseCase


@ddt
class TestBaidu(BaseCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @file_data("../../data/template/template.yaml")
    def test_01_search(self, **kwargs): ...
