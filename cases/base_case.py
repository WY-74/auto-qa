from config.chrome_options import get_driver
from utils import Utils


class BaseCase:
    @classmethod
    def setup_class(cls):
        cls.driver = get_driver()
        cls.helper = Utils()

    @classmethod
    def teardown_class(self):
        self.driver.quit()
