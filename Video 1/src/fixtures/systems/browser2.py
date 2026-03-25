from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest


@pytest.fixture()
def set_up_browser2():
    chrome_options = Options()
    chrome_options.set_capability("browserVersion", "latest")

    driver = webdriver.Remote(
        command_executor="http://127.0.0.1:4444/wd/hub",
        options=chrome_options  # используем options вместо desired_capabilities
    )
    return driver