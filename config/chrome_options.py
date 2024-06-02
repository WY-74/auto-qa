from selenium import webdriver
from config.log import logger


def chrome_options():
    options = webdriver.ChromeOptions()

    options.page_load_strategy = "normal"

    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option(
        "prefs", {"credentials_enable_service": False, "profile.password_manager_enable": False}
    )

    options.add_argument("start-maximized")
    options.add_argument("--log_level=3")
    options.add_argument("--disable-gup")
    options.add_argument("--ignore-certificate-errors")

    logger.debug(f"{options.to_capabilities()}")

    return options


def get_driver(driver_type: str | None = None):
    """
    bowser_type:
        Chrome: Chrome, chrome, Googel Chrome, google chrome
    """

    browser_map = {"Chrome": ["Chrome", "chrome", "Googel Chrome", "google chrome"]}
    driver = None

    for key, value in browser_map.items():
        if driver_type in value:
            driver_type = key
            driver = getattr(webdriver, driver_type)()
            break

    if driver is None:
        driver_type = "Chrome"
        driver = webdriver.Chrome(options=chrome_options())

    driver.implicitly_wait(5)

    logger.info("init driver finished")

    return driver
