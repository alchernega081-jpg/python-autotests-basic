from symbol import pass_stmt
from time import sleep

from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


# Определение фикстуры
@pytest.fixture
def selenium():
    driver = webdriver.Chrome()  # или другой браузер
    yield driver
    driver.quit()


class TestWait:
    def test_wait_page_load(self, selenium):
        selenium = selenium  # ← обратите внимание на отступ
        selenium.get("http://github.com")
        selenium.find_element(
            By.XPATH, '//*[contains(text(), "The future of building happens together")]'
        )
        # Здесь может быть ваш код для тестирования

    def test_wait_types(self, selenium):
        selenium = selenium  # ← обратите внимание на отступ
        selenium.get("http://github.com")
        # driver.find_element(By.XPATH, '//*[contains(text(), "The future of building happens together")]')
        # Здесь может быть ваш код для тестирования
        WebDriverWait(selenium, timeout=3).until(
            lambda d: d.find_element(
                By.XPATH,
                '//*[contains(text(), "The future of building happens together")]',
            )
        )

    def test_wait_dialof(self, selenium):
        selenium.get("https://m1vcki.csb.app/")
        WebDriverWait(selenium, timeout=30).until(
            lambda d: d.find_element(By.ID, "name")
        )
        # sleep(30)
        selenium.find_element(By.ID, "name").send_keys("skillbox")
        selenium.find_element(By.ID, "email").send_keys("skillbox@mail.ru")
        selenium.find_element(By.NAME, "password").send_keys("skillbox")
        selenium.execute_script("document.activeElement.blur()")
        selenium.find_element(By.CSS_SELECTOR, '[role="checkbox"]').click()
        selenium.find_element(
            By.XPATH, '//button/span[contains(text(), "Submit")]'
        ).click()
        # driver.find_element(By.XPATH, '//button/span[contains(text(), "Ok")]').click()
        # selenium.find_element(By.XPATH, '//*[contains(text(), "The future of building happens together")]')
        # Здесь может быть ваш код для тестирования
        WebDriverWait(selenium, timeout=5).until(
            lambda d: d.find_element(By.XPATH, '//button/span[contains(text(), "OK")]')
        )
        selenium.find_element(By.XPATH, '//button/span[contains(text(), "OK")]').click()

    pass
