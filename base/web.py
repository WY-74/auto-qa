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


class Timeout(object):
    SHORT_TIMEOUT = 5
    MEDIUM_TIMEOUT = 12
    LONG_TIMEOUT = 30
    MAX_PAGE_LOAD_TIMEOUT = 60
    NO_TIMEOUT = 0


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
        self.logger.debug(locals())

        elements = self.get_elements(locator, index=index, root=root)
        if not elements:
            msg = f"no element found by {locator}"
            self.logger.error(msg)
            raise ValueError(msg)

        def click_one(_elem):
            self.logger.info("click start")

            if use_action_chain:
                self.logger.info("click with action chain")
                ActionChains(self.driver).move_to_element(_elem).perform()
            time.sleep(wait_to)
            _elem.click()
            self.logger.info("click finished")
            return True

        if isinstance(elements, list):
            for elem in elements:
                if click_one(elem):
                    return True
        else:
            return click_one(elements)

    def click_with_js(
        self,
        locator: str | tuple | WebElement,
        index: int | None = 0,
        root: WebDriver | WebElement | None = None,
    ):
        self.logger.debug(locals())

        elements = self.get_elements(locator, index=index, root=root)
        if not elements:
            msg = f"no element found by {locator}"
            self.logger.error(msg)
            raise ValueError(msg)

        def click_one(_elem):
            self.logger.info("click_with_js start")
            self.driver.execute_script("(arguments[0]).click();", elements)
            self.logger.info("click_with_js finished")
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
        self.logger.info("dump_cookies finished")

    def get_elements_attribute(
        self,
        locator: str | tuple | WebElement,
        attribute: str = "innerText",
        index: int | None = 0,
        root: WebDriver | WebElement | None = None,
    ):
        self.logger.debug(locals())

        elems = self.get_elements(locator)
        if not elems:
            msg = f"no element found by {locator}"
            self.logger.error(msg)
            raise ValueError(msg)

        self.logger.info("get_elements_attribute start")
        if index is None:
            attrs = [elem.get_attribute(attribute) for elem in elems]
        else:
            attrs = elems.get_attribute(attribute)
        self.logger.info("get_elements_attribute finished")
        return attrs

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
        self.logger.debug(locals())

        self.logger.info("get_elements start")
        if not isinstance(locator, tuple) and not isinstance(locator, str):
            return locator
        if isinstance(locator, str):
            locator = (By.CSS_SELECTOR, locator)

        root = root or self.driver
        try:
            elements = root.find_elements(*locator)

            if elements and isinstance(index, int):
                elements = elements[index]

            self.logger.info("get_elements finished")
            return elements
        except WebDriverException as e:
            self.logger.error(f"get {locator} failed with {e}")
            raise e

    def get_elements_by_children(self, locator: str | tuple | WebElement, child_locator: str | tuple):
        self.logger.debug(locals())

        if isinstance(child_locator, WebElement):
            msg = f"child_locator must be str or tuple, now is {type(child_locator)}"
            self.logger.error(msg)
            raise ValueError(msg)

        elems = self.get_elements(locator, index=None)

        self.logger.info("get_elements_by_children start")
        children = []
        for elem in elems:
            children.extend(self.get_elements(child_locator, index=None, root=elem))
        self.logger.info("get_elements_by_children finished")
        return children

    def load_cookies(self, path: str = "config/auto-qa.cookies"):
        cookie_file = Path(path)
        if not cookie_file.exists():
            msg = f"cookie not found locally, please check the path: {cookie_file}"
            self.logger.error(msg)
            raise ValueError(msg)

        data = cookie_file.read_text()
        cookies = json.loads(data)
        self.logger.debug(f"loaded {len(cookies)} cookies to driver")
        for ck in cookies:
            self.driver.add_cookie(ck)

        self.logger.info("load_cookies finished")

    def must_get_attribute(
        self,
        locator: str | tuple | WebElement,
        attribute: str = "innerText",
        index: int | None = 0,
        root: WebDriver | WebElement | None = None,
    ):
        self.logger.debug(locals())

        elems = self.must_get_element(locator, index=index)

        self.logger.info("must_get_attribute start")
        if isinstance(elems, list):
            attrs = [elem.get_attribute(attribute) for elem in elems]
        else:
            attrs = elems.get_attribute(attribute)
        self.logger.info("must_get_attribute finished")
        return attrs

    def must_get_element(
        self,
        locator: str | tuple | WebElement,
        index: int = 0,
        root: WebDriver | WebElement | None = None,
        timeout: int = Timeout.LONG_TIMEOUT,
        ignored_exceptions=(TimeoutException,),
    ) -> bool:
        self.logger.debug(locals())

        try:
            self.logger.info("must_get_element start")
            getattr(WebDriverWait(self, timeout=timeout, ignored_exceptions=ignored_exceptions), "until")(
                lambda x: x.get_elements(locator, index=index, root=root)
            )
        except ignored_exceptions as ie:
            msg = f"no element found by {locator}"
            self.logger.error(msg)
            raise ie

        self.logger.info("must_get_element finished")
        return True

    def must_no_element(
        self,
        locator: str | tuple | WebElement,
        index: int = 0,
        root: WebDriver | WebElement | None = None,
        timeout: int = Timeout.LONG_TIMEOUT,
    ):
        self.logger.debug(locals())

        try:
            self.logger.info("most_no_element start")
            getattr(WebDriverWait(self, timeout=timeout), "until_not")(
                lambda x: x.get_elements(locator, index=index, root=root)
            )
        except TimeoutException as e:
            msg = f"element with {locator} is existence"
            self.logger.error(msg)
            raise e

        self.logger.info("most_no_element finished")
        return True

    def navigate(self, url: str):
        if url in self.driver.current_url:
            return
        self.driver.get(url)
        self.logger.info(f"navigate to {url} finished")

    def refresh(self):
        self.driver.refresh()

    def scroll_and_click(
        self, locator: str | tuple | WebElement, index: int | None = 0, root: WebDriver | WebElement | None = None
    ) -> bool:
        self.logger.debug(locals())

        element = self.get_elements(locator, index=index, root=root)
        if not element:
            msg = f"no element found by {locator}"
            self.logger.error(msg)
            raise ValueError(msg)

        self.scroll_to_element(element)
        self.click(element)
        self.logger.info("scroll_and_click finished")

    def scroll_to_element(self, element: WebElement, is_window=True, steps: float | int = 8):
        self.logger.debug(locals())

        self.logger.info("scroll_to_element start")
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

        self.logger.info("scroll_to_element finished")

    def update_text(
        self,
        locator: str | tuple | WebElement,
        value: str,
        index: int | None = 0,
        root: WebDriver | WebElement | None = None,
    ):
        self.logger.debug(locals())

        elem = self.get_elements(locator, index=index, root=root)
        if not elem:
            msg = f"no element found by {locator}"
            self.logger.error(msg)
            raise ValueError(msg)

        if not isinstance(elem, WebElement):
            msg = f"{locator=}'s should only find one WebElement"
            self.logger.error(msg)
            raise TypeError(f"{locator=}'s should only find one WebElement")

        self.logger.info("update_text start")
        elem.send_keys(value)
        self.logger.info("update_text finished")
        return True

    # ensure_and_highlight_element
    # switch_to_window
