from config.chrome_options import get_driver
from config.credentials import credentials


class BaseCase:
    @classmethod
    def setup_class(cls):
        cls.credentials = credentials
        cls.driver = get_driver()

    @classmethod
    def teardown_class(self):
        self.driver.quit()
