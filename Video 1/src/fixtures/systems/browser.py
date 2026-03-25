import logging
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options
import pytest


#def pytest_addoption(parser): по заданию удалено и перенесено в conftest.py
 #   parser.addini("selenium_url", "Selenium Hub url")
 #  parser.addini("browser_name", "Browser name for tests")
 #   parser.addini("browser_version", "Browser version for tests")
    #parser.addini("headless", "Run browser in headless mode", default="False")  # добавляем headless


@pytest.fixture()
def selenium(pytestconfig):
    chrome_options = Options()
    chrome_options.page_load_strategy = 'normal'

    # Раскомментируем эту строку
    browser_name = pytestconfig.getini("browser_name")

    logging.info(f'Prepare {browser_name} browser...')

    # Проверяем headless режим
    #if pytestconfig.getini("headless") == 'True' and browser_name == "chrome":
     #   chrome_options.add_argument("--headless")

    chrome_options.set_capability("browserName", browser_name)
    chrome_options.set_capability("browserVersion", pytestconfig.getini("browser_version"))

    driver = Remote(
        command_executor=pytestconfig.getini("selenium_url"),
        options=chrome_options
    )
    logging.info(f'Browser {browser_name} has been started...')
    yield driver
    driver.quit()


@pytest.fixture()
def new_fixture():
    pass