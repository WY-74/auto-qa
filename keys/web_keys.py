from selenium import webdriver
from time import sleep
from typing import Any
from config.chrome_options import chrome_options


def open_browser(browser_type: str | None):
    """
    bowser_type:
        Chrome: Chrome, chrome, Googel Chrome, google chrome
    """

    browser_map = {"Chrome": ["Chrome", "chrome", "Googel Chrome", "google chrome"]}

    for key, value in browser_map.items():
        if browser_type in value:
            return getattr(webdriver, key)()

    return webdriver.Chrome(options=chrome_options())


class WebKeys:
    def __init__(self, browser_type: str | None = None):
        self.driver = open_browser(browser_type)
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
