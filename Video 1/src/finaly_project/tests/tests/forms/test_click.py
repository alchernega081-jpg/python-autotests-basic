import time
from symbol import pass_stmt
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


class TestClick:
    def test_click(self, selenium):
        selenium.get('https://demoqa.com/modal-dialogs')
        selenium.find_element(By.XPATH, '//*[@id="showSmallModal"]').click()

    def test_failed_click(self, selenium):
        selenium.get('https://demoqa.com/buttons')
        selenium.find_element(By.XPATH, '//button').click()

    def test_double_click(self, selenium):
        selenium.get('https://demoqa.com/buttons')
        action_chains = webdriver.ActionChains(selenium)
        action_chains.double_click()
        action_chains.double_click(selenium.find_element(By.ID, "doubleClickBtn")).perform()
        action_chains.double_click(selenium.find_element(By.ID, "doubleClickBtn")).perform()

    def test_checkboks(self, selenium):
        selenium.get('https://demoqa.com/automation-practice-form')
        selenium.find_element(By.ID, 'hobbies-checkbox-1').click()
        selenium.find_element(By.ID, 'hobbies-checkbox-2').click()
        selenium.find_element(By.ID, 'hobbies-checkbox-3').click()

    def test_rodiobutton(self, selenium):
        selenium.get('https://demoqa.com/radio-button')
        selenium.find_element(By.ID, 'yesRadio').click()

    def test_click(self, selenium):
        selenium.get('https://demoqa.com/modal-dialogs')
        selenium.find_element(By.XPATH, '//*[@id="showSmallModal"]').click()
        selenium.find_element(By.XPATH, '//button[text()="Close"]').click()

    def test_button_dropdown(self, selenium):
        selenium.get('https://demoqa.com/select-menu')
        selenium.find_element(By.ID, 'react-select-2-input').click()
        option = WebDriverWait(selenium, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[text()="Group 1, option 1"]'))
        )
        option.click()

    def test_calendar(self, selenium):
        selenium.get('https://demoqa.com/date-picker')
        selenium.find_element(By.ID, 'datePickerMonthYearInput').click()
        #selenium.find_element(By.ID, 'datePickerMonthYearInput').click()
        pass

