from time import sleep
from typing import Any


class WebKeys:
    def __init__(self, driver):
        self.driver = driver

    def accept_alert(self, text: str | None = None):
        _alert = self.driver.switch_to.alert
        if text:
            _alert.send_keys(text)
        _alert.accept()

    def assert_text_equal(self, locator: tuple, expect: str):
        actual = self.locator(locator).text
        assert actual == expect, f"actual: {actual} != expect: {expect}"

    def click(self, locator):
        self.locator(locator).click()

    def close(self):
        self.driver.quit()

    def dismiss_alert(self, text: str | None = None):
        _alert = self.driver.switch_to.alert
        if text:
            _alert.send_keys(text)
        _alert.dismiss()

    def get_alert_prompt(self):
        return self.driver.switch_to.alert.text

    def get_url(self):
        return self.driver.current_url

    def input(self, locator: tuple, txt: str):
        self.locator(locator).send_keys(txt)

    def locator(self, locator: tuple):
        return self.driver.find_element(*locator)

    def open(self, url: str):
        self.driver.get(url)

    def wait(self, times: Any):
        sleep(int(times))
