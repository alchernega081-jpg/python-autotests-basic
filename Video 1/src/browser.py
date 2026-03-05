from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options
import pytest


@pytest.fixture()
def set_up_browser():
    chrome_options = Options()
    chrome_options.set_capability("browserVersion", "latest")

    driver = Remote(
        command_executor="http://127.0.0.1:4444/wd/hub",
        desired_capabilities=chrome_options.to_capabilities()
    )
    yield driver
    driver.quit()

