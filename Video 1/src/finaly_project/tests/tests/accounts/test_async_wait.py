import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import logging

from src.helpers.accounts_base import AccountsBase

# Создаем логгер для этого модуля
logger = logging.getLogger("request")


@allure.feature("Тестирование ожиданий на веб-страницах")
@allure.story("Проверка различных типов ожиданий в Selenium")
class TestAsyncWait(AccountsBase):

    @allure.title("Проверка загрузки главной страницы GitHub")
    @allure.description(
        "Тест проверяет, что главная страница GitHub успешно загружается и содержит ожидаемый текст"
    )
    def test_wait_page_load(self, selenium, go_to_github):
        with allure.step("Открытие главной страницы GitHub"):
            logger.info("Starting test: test_wait_page_load")
            # go_to_github уже открывает страницу, используем её
            pass

        with allure.step(
            'Поиск элемента с текстом "The future of building happens together"'
        ):
            logger.info(
                "Searching for element with text: 'The future of building happens together'"
            )
            element = selenium.find_element(
                By.XPATH,
                '//*[contains(text(), "The future of building happens together")]',
            )
            allure.attach(
                element.text,
                name="Найденный текст элемента",
                attachment_type=allure.attachment_type.TEXT,
            )
            logger.info("Successfully found element on page")

        with allure.step("Проверка успешного отображения контента"):
            assert element.is_displayed(), "Элемент не отображается на странице"
            logger.info("Element is displayed correctly")

    @allure.title("Проверка явного ожидания загрузки элемента")
    @allure.description(
        "Тест проверяет работу WebDriverWait для ожидания появления элемента на странице"
    )
    def test_wait_types(self, selenium):
        with allure.step("Открытие главной страницы GitHub"):
            logger.info("Starting test: test_wait_types")
            url = "http://github.com"
            logger.info(f"Navigating to URL: {url}")
            selenium.get(url)
            allure.attach(
                selenium.current_url,
                name="Текущий URL после навигации",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step(
            "Ожидание появления элемента с текстом (WebDriverWait, timeout=3 сек)"
        ):
            logger.info("Waiting for element to be present with timeout 3 seconds")
            element = WebDriverWait(selenium, timeout=3).until(
                lambda d: d.find_element(
                    By.XPATH,
                    '//*[contains(text(), "The future of building happens together")]',
                )
            )
            logger.info("Element found successfully")
            allure.attach(
                "Элемент найден в течение 3 секунд",
                name="Результат ожидания",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Проверка отображения найденного элемента"):
            assert element.is_displayed(), "Элемент должен отображаться на странице"
            logger.info("Element is visible and test passed")

    @allure.title("Проверка работы с диалоговым окном")
    @allure.description(
        "Тест проверяет заполнение формы и взаимодействие с модальным диалогом"
    )
    def test_wait_dialog(self, selenium):
        with allure.step("Открытие тестовой страницы с формой"):
            logger.info("Starting test: test_wait_dialog")
            url = "https://m1vcki.csb.app/"
            logger.info(f"Navigating to URL: {url}")
            selenium.get(url)
            allure.attach(
                url,
                name="URL тестовой страницы",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Ожидание загрузки поля ввода имени"):
            logger.info("Waiting for name input field to be present")
            name_field = WebDriverWait(selenium, timeout=30).until(
                EC.presence_of_element_located((By.ID, "name"))
            )
            allure.attach(
                "Поле ввода имени загружено",
                name="Статус загрузки",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Заполнение формы регистрации"):
            logger.info("Filling form fields...")

            with allure.step("Ввод имени"):
                selenium.find_element(By.ID, "name").send_keys("skillbox")
                allure.attach(
                    "skillbox",
                    name="Введенное имя",
                    attachment_type=allure.attachment_type.TEXT,
                )

            with allure.step("Ввод email"):
                selenium.find_element(By.ID, "email").send_keys("skillbox@mail.ru")
                allure.attach(
                    "skillbox@mail.ru",
                    name="Введенный email",
                    attachment_type=allure.attachment_type.TEXT,
                )

            with allure.step("Ввод пароля"):
                selenium.find_element(By.NAME, "password").send_keys("skillbox")
                allure.attach(
                    "********",
                    name="Введенный пароль",
                    attachment_type=allure.attachment_type.TEXT,
                )

            with allure.step("Снятие фокуса с активного элемента"):
                selenium.execute_script("document.activeElement.blur()")
                logger.info("Blur executed on active element")

            with allure.step("Клик по чекбоксу"):
                selenium.find_element(By.CSS_SELECTOR, '[role="checkbox"]').click()
                logger.info("Checkbox clicked")
                allure.attach(
                    "Чекбокс выбран",
                    name="Статус чекбокса",
                    attachment_type=allure.attachment_type.TEXT,
                )

        with allure.step("Отправка формы"):
            logger.info("Submitting form")
            submit_button = selenium.find_element(
                By.XPATH, '//button/span[contains(text(), "Submit")]'
            )
            submit_button.click()
            logger.info("Form submitted successfully")
            allure.attach(
                "Форма отправлена",
                name="Действие",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Ожидание появления кнопки OK в диалоговом окне"):
            logger.info("Waiting for OK button to appear")
            ok_button = WebDriverWait(selenium, timeout=5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//button/span[contains(text(), "OK")]')
                )
            )
            logger.info("OK button found")
            allure.attach(
                "Кнопка OK появилась",
                name="Статус ожидания",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Нажатие на кнопку OK для закрытия диалога"):
            logger.info("Clicking OK button")
            ok_button.click()
            logger.info("Dialog closed successfully")
            allure.attach(
                "Диалоговое окно закрыто",
                name="Результат",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Проверка успешного завершения теста"):
            logger.info("Test completed successfully")
            allure.attach(
                "Все шаги теста выполнены успешно",
                name="Итог теста",
                attachment_type=allure.attachment_type.TEXT,
            )
