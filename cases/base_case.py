import unittest
from config.chrome_options import get_driver


class BaseCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
