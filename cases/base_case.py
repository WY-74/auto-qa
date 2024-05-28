from config.chrome_options import get_driver


class BaseCase:
    @classmethod
    def setup_class(cls):
        cls.driver = get_driver()

    @classmethod
    def teardown_class(self):
        self.driver.quit()
