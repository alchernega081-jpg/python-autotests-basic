from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_driver():
    # webdriver-manager сам скачает нужную версию ChromeDriver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Для CI обычно нужен headless режим
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=service, options=options)
    return driver






#from selenium.webdriver import Remote
#from selenium.webdriver.chrome.options import Options
#import pytest


#@pytest.fixture()
#def set_up_browser():
    #chrome_options = Options()
    #chrome_options.set_capability("browserVersion", "latest")

    #driver = Remote(
        #command_executor="http://127.0.0.1:4444/wd/hub",
        #desired_capabilities=chrome_options.to_capabilities()
    #)
    #yield driver
    #river.quit()

