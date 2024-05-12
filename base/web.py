from time import sleep
from typing import Any
from config.chrome_options import get_driver


class WebKeys:
    def __init__(self, browser_type: str | None = None):
        self.driver = get_driver(browser_type)
        self.driver.implicitly_wait(10)

    def accept_alert(self, text: str | None = None):
        _alert = self.driver.switch_to.alert
        if text:
            _alert.send_keys(text)
        _alert.accept()

    def assert_text_equal(self, by: str, value: str, expect: str):
        actual = self.locator(by=by, value=value).text
        assert actual == expect, f"actual: {actual} != expect: {expect}"

    def click(self, by: str, value: str):
        self.locator(by, value).click()

    def close(self):
        self.driver.quit()

    def dismiss_alert(self, text: str | None = None):
        _alert = self.driver.switch_to.alert
        if text:
            _alert.send_keys(text)
        _alert.dismiss()

    def get_alert_prompt(self):
        return self.driver.switch_to.alert.text

    def input(self, by: str, value: str, txt: str):
        self.locator(by, value).send_keys(txt)

    def locator(self, by: str, value: str):
        return self.driver.find_element(by=by, value=value)

    def open(self, url: str):
        self.driver.get(url)

    def wait(self, times: Any):
        sleep(int(times))
