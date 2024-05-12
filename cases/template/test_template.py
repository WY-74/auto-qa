import unittest
from ddt import ddt, file_data
from config.chrome_options import get_driver


@ddt
class TestBaidu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    @file_data("../data/template/template.yaml")
    def test_01_search(self, **kwargs): ...
