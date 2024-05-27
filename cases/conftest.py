import pytest
from config.chrome_options import get_driver


@pytest.fixture(scope='module')
def controller(request):
    def driver_finalizer():
        driver.quit()

    request.addfinalizer(driver_finalizer)

    driver = get_driver()
    return driver
