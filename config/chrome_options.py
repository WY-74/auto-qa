import configparser
from selenium import webdriver
from config.log import logger


def chrome_options(headless: bool = False, download_to: str = ""):
    options = webdriver.ChromeOptions()

    options.page_load_strategy = "normal"

    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    prefs = {
        "profile.password_manager_enabled": False,
        "credentials_enable_service": False,
        "download.default_directory": download_to,
    }
    options.add_experimental_option("prefs", prefs)

    options.add_argument("start-maximized")
    options.add_argument("--log_level=3")
    options.add_argument("--disable-gup")
    options.add_argument("--ignore-certificate-errors")
    if bool(headless):
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

    logger.debug(f"{options.to_capabilities()}")
    return options


def get_driver():
    """
    Supported Browsers:
        - Chrome
    """
    _config = configparser.ConfigParser()
    _config.read('.\pytest.ini', encoding="utf-8")
    _config = dict(_config.items("driver"))
    headless = False if _config["headless"] == "False" else True
    download_to = _config["download_to"]

    driver = webdriver.Chrome(options=chrome_options(headless, download_to))
    driver.implicitly_wait(5)

    logger.info("init driver finished")
    return driver
