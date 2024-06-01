import json
import time
from typing import List
from config.log import logger
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException


class WebKeys:
    def __init__(self, driver: WebDriver | None = None):
        self.driver = driver
        self.logger = logger
        self.logger.info("init webkeys finished")

    def click(
        self,
        locator: str | tuple | WebElement,
        index: int | None = 0,
        use_action_chain: bool = False,
        root: WebDriver | WebElement | None = None,
        wait_to: float | int = 0.1,
    ) -> bool:
        elements = self.get_elements(locator, index=index, root=root)
        if not elements:
            msg = f"no element with {locator} is found"
            self.logger.error(msg)
            raise ValueError(msg)

        def click_one(_elem):
            if use_action_chain:
                self.logger.debug("click use action chain")
                ActionChains(self.driver).move_to_element(_elem).perform()
            time.sleep(wait_to)
            _elem.click()
            return True

        if isinstance(elements, list):
            for elem in elements:
                if click_one(elem):
                    return True
        else:
            return click_one(elements)

    def dump_cookies(self, path: str = "config/auto-qa.cookies"):
        # Note: If "auto-qa.cookies" already exists, the original information will be overwritten when this method is called again.
        cookies = self.driver.get_cookies()
        self.logger.debug(f"dumped {len(cookies)} cookies to {path}")
        Path(path).write_text(json.dumps(cookies, indent=4))

    def get_elements(
        self, locator: str | tuple | WebElement, index: int | None = 0, root: WebDriver | WebElement | None = None
    ) -> WebElement | List[WebElement] | None:
        """
        first of all get_elements will always find multiple elems,
        if index is None, will return all found elems
        else just return the element with supplied index.

        there 3 types of return value:
            1. nothing found, just return elems which is []
            2. index is None = multiple elems, just return elems
            3. index is int = not multiple, just return elems[index]
        """
        if not isinstance(locator, tuple) and not isinstance(locator, str):
            return locator

        if isinstance(locator, str):
            locator = (By.CSS_SELECTOR, locator)

        self.logger.debug(f"find elements by {locator}")

        root = root or self.driver
        try:
            elements = root.find_elements(*locator)

            if index is None:
                return elements

            if elements and isinstance(index, int):
                return elements[index]
        except WebDriverException as e:
            self.logger.error(f"get {locator} failed with {e}")
            raise

    def load_cookies(self, path: str = "config/auto-qa.cookies"):
        cookie_file = Path(path)
        if not cookie_file.exists():
            self.logger.debug(f"cookie not found locally, please check the path: {cookie_file}")
            return
        data = cookie_file.read_text()
        cookies = json.loads(data)
        self.logger.debug(f"loaded {len(cookies)} cookies to driver")
        for ck in cookies:
            self.driver.add_cookie(ck)

    def must_get_element(
        self,
        locator: str | tuple | WebElement,
        index: int = 0,
        root: WebDriver | WebElement | None = None,
        timeout: int = 30,
        ignored_exceptions=(TimeoutException,),
    ) -> bool:
        try:
            getattr(WebDriverWait(self, timeout=timeout, ignored_exceptions=ignored_exceptions), "until")(
                lambda x: x.get_elements(locator, index=index, root=root)
            )
        except ignored_exceptions as ie:
            msg = f"no element with {locator} is found"
            self.logger.error(msg)
            raise ie

        return True

    def refresh(self):
        self.driver.refresh()

    def scroll_and_click(
        self, locator: str | tuple | WebElement, index: int | None = 0, root: WebDriver | WebElement | None = None
    ) -> bool:
        element = self.get_elements(locator, index=index, root=root)
        if not element:
            msg = f"no element with {locator} is found"
            self.logger.error(msg)
            raise ValueError(msg)

        self.scroll_to_element(element)
        return self.click(element)

    def scroll_to_element(self, element: WebElement, is_window=True, steps: float | int = 8):
        try:
            element_location = element.location['y']
        except Exception:
            return element.location_once_scrolled_into_view

        element_location = element_location - 130
        if element_location < 0:
            element_location = 0
        if is_window:
            scroll_script = "window.scrollTo(0, %s);" % element_location
        else:
            scroll_script = "(arguments[0]).scrollBy(0, {})".format(steps)

        try:
            self.driver.execute_script(scroll_script, element)
        except WebDriverException:
            pass

    def update_text(
        self,
        locator: str | tuple | WebElement,
        value: str,
        index: int | None = 0,
        root: WebDriver | WebElement | None = None,
    ):
        elem = self.get_elements(locator, index=index, root=root)
        if not elem:
            msg = f"no input element with {locator} is found"
            self.logger.error(msg)
            raise ValueError(msg)

        if not isinstance(elem, WebElement):
            msg = f"{locator=}'s should only find one WebElement"
            self.logger.error(msg)
            raise TypeError(f"{locator=}'s should only find one WebElement")

        elem.send_keys(value)
        return True

    #########

    def accept_alert(self, text: str | None = None):
        _alert = self.driver.switch_to.alert
        if text:
            _alert.send_keys(text)
        _alert.accept()

    def assert_text_equal(self, locator: tuple, expect: str):
        actual = self.locator(locator).text
        assert actual == expect, f"actual: {actual} != expect: {expect}"

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

    def open(self, url: str):
        self.driver.get(url)
