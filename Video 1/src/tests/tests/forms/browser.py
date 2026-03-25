from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options
import pytest


#def pytest_addoption(parser):
    #parser.addini("selenium_url", "Selenium Hub url")
    #parser.addini("browser_name", "Browser name for tests")
    #parser.addini("browser_version", "Browser version for tests")
    #parser.addini("headless", "Run browser in headless mode", default="False")  # добавляем headless


@pytest.fixture()
def selenium(pytestconfig):
    chrome_options = Options()
    chrome_options.page_load_strategy = 'normal'

    # Исправляем: используем chrome_options вместо options
    #browser_name = pytestconfig.getini("browser_name")
    #if pytestconfig.getini("headless") == 'True' and browser_name == "chrome":
        #chrome_options.add_argument("--headless")  # было options.add_argument


    chrome_options.set_capability("browserName", pytestconfig.getini("browser_name"))
    chrome_options.set_capability("browserVersion", pytestconfig.getini("browser_version"))

    driver = Remote(
        command_executor=pytestconfig.getini("selenium_url"),
        options=chrome_options
    )

    yield driver
    driver.quit()
