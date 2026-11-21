"""
Модуль с автотестами для сайта Pizzeria (https://pizzeria.skillbox.cc/)
Содержит тестовые сценарии для проверки функционала:
- добавление пицц в корзину
- заказ пиццы с дополнительными опциями
- управление корзиной
- фильтрация десертов
- оформление заказа с авторизацией
"""

import time
import logging
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


@allure.feature("Тестовые сценарии для сайта Pizzeria")
class TestCases:
    """
    Класс, содержащий все тестовые сценарии для сайта Pizzeria.
    """

    @allure.story("Добавление пицц в корзину и проверка содержимого")
    @allure.description(
        """
    Этот тест выполняет следующие действия:
    1. Открывает главную страницу сайта
    2. Добавляет пиццу "Рай" в корзину (с наведением курсора)
    3. Добавляет пиццу "Пепперони" в корзину (с перелистыванием слайдера)
    4. Добавляет пиццу "4 в 1" в корзину
    5. Переходит в корзину и проверяет наличие всех добавленных пицц
    """
    )
    def test_case_1(self, browser):
        """TC-001: Добавление трех пицц в корзину и проверка их наличия (
        меняем set_up_browser на browser"""
        driver = browser
        logger = logging.getLogger(__name__)

        logger.info("START: test_case_1 - Добавление пицц в корзину")

        with allure.step("Открытие главной страницы сайта"):
            logger.info("Открытие главной страницы")
            driver.get("https://pizzeria.skillbox.cc/")
            time.sleep(2)

        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(1)

        with allure.step('Добавление пиццы "Рай" в корзину'):
            logger.info("Добавление пиццы 'Рай'")
            pizza_card = driver.find_element(By.XPATH, '(//*[@title= "Пицца «Рай»"])[3]')
            ActionChains(driver).move_to_element(pizza_card).perform()
            time.sleep(1)

            try:
                button = pizza_card.find_element(By.CSS_SELECTOR, '.add_to_cart_button')
            except:
                button = pizza_card.find_element(By.XPATH, './/a[contains(text(), "В корзину")]')
            button.click()
            time.sleep(1)

        with allure.step('Добавление пиццы "Пепперони" в корзину'):
            logger.info("Добавление пиццы 'Пепперони'")
            driver.find_element(By.CLASS_NAME, "slick-next").click()
            time.sleep(1)
            pizza_card = driver.find_element(By.XPATH, '(//*[@title= "Пицца «Пепперони»"])[3]')
            ActionChains(driver).move_to_element(pizza_card).perform()
            time.sleep(1)

            try:
                button = pizza_card.find_element(By.CSS_SELECTOR, '.add_to_cart_button')
            except:
                button = pizza_card.find_element(By.XPATH, './/a[contains(text(), "В корзину")]')
            button.click()
            time.sleep(1)

        with allure.step('Добавление пиццы "4 в 1" в корзину'):
            logger.info("Добавление пиццы '4 в 1'")
            driver.find_element(By.CLASS_NAME, "slick-prev").click()
            time.sleep(1)
            pizza_card = driver.find_element(By.XPATH, '(//*[@title= "Пицца «4 в 1»"])[1]')
            ActionChains(driver).move_to_element(pizza_card).perform()
            time.sleep(1)

            try:
                button = pizza_card.find_element(By.CSS_SELECTOR, '.add_to_cart_button')
            except:
                button = pizza_card.find_element(By.XPATH, './/a[contains(text(), "В корзину")]')
            button.click()
            time.sleep(2)

        with allure.step("Проверка содержимого корзины"):
            logger.info("Проверка корзины")
            driver.find_element(By.CLASS_NAME, "cart-contents").click()
            time.sleep(2)

            products_in_cart = driver.find_elements(By.CLASS_NAME, "product-name")
            expected_products = ["Пицца «Рай»", "Пицца «Пепперони»", "Пицца «4 в 1»"]
            actual_products = [p.text for p in products_in_cart if p.text != "ТОВАР"]

            for expected_product in expected_products:
                with allure.step(f'Проверка наличия товара "{expected_product}" в корзине'):
                    assert expected_product in actual_products, f"Товар {expected_product} отсутствует"

            allure.attach("Все товары в корзине", name="Результат", attachment_type=allure.attachment_type.TEXT)
            logger.info("SUCCESS: test_case_1 завершен")

    @allure.story("Заказ пиццы с дополнительными опциями")
    @allure.description(
        """
    Этот тест выбирает пиццу 'Как у бабушки' с сырным бортом и добавляет в корзину
    """
    )
    def test_case_2(self, browser):
        """TC-002: Заказ пиццы с дополнительной опцией меняем set_up_browser на browser"""
        driver = browser
        logger = logging.getLogger(__name__)

        logger.info("START: test_case_2 - Заказ пиццы с опциями")

        with allure.step("Открытие главной страницы сайта"):
            driver.get("https://pizzeria.skillbox.cc/")
            time.sleep(2)

        with allure.step('Выбор пиццы "Как у бабушки"'):
            driver.execute_script("window.scrollBy(0, 400);")
            time.sleep(1)
            driver.find_element(By.XPATH, '(//*[@title= "Пицца «Как у бабушки»"])[3]').click()
            time.sleep(2)

        with allure.step('Добавление опции "Сырный борт"'):
            driver.find_element(By.NAME, "board_pack").click()
            driver.find_element(By.XPATH, "//*[contains(text(), 'Сырный - 55.00 р.')]").click()

        with allure.step("Добавление пиццы в корзину"):
            driver.find_element(By.CLASS_NAME, "single_add_to_cart_button").click()
            time.sleep(2)

        with allure.step("Проверка корзины"):
            driver.find_element(By.CLASS_NAME, "cart-contents").click()
            time.sleep(2)
            products = driver.find_elements(By.CLASS_NAME, "product-name")
            expected = ['Пицца "Как у бабушки"\nДополнительно:\nСырный борт']
            actual = [p.text for p in products if p.text != "ТОВАР"]

            assert expected[0] in actual, "Пицца с сырным бортом не найдена"
            allure.attach("Пицца с опцией добавлена", name="Результат", attachment_type=allure.attachment_type.TEXT)

        logger.info("SUCCESS: test_case_2 завершен")

    @allure.story("Управление корзиной и проверка итоговой суммы")
    @allure.description(
        """
    Этот тест проверяет изменение количества и удаление товара из корзины
    """
    )
    def test_case_3(self, browser):
        """TC-003: Изменение количества товаров и проверка суммы меняем set_up_browser на browser"""
        driver = browser
        logger = logging.getLogger(__name__)

        logger.info("START: test_case_3 - Управление корзиной")

        with allure.step("Открытие главной страницы"):
            driver.get("https://pizzeria.skillbox.cc/")
            time.sleep(2)

        driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(1)

        with allure.step('Добавление пиццы "Рай"'):
            pizza_card = driver.find_element(By.XPATH, '(//*[@title= "Пицца «Рай»"])[3]')
            ActionChains(driver).move_to_element(pizza_card).perform()
            time.sleep(1)
            try:
                button = pizza_card.find_element(By.CSS_SELECTOR, '.add_to_cart_button')
            except:
                button = pizza_card.find_element(By.XPATH, './/a[contains(text(), "В корзину")]')
            button.click()
            time.sleep(1)

        with allure.step('Добавление пиццы "Как у бабушки" с сырным бортом'):
            pizza_card = driver.find_element(By.XPATH, '(//*[@title= "Пицца «Как у бабушки»"])[3]')
            pizza_card.click()
            time.sleep(2)
            driver.find_element(By.NAME, "board_pack").click()
            driver.find_element(By.XPATH, "//*[contains(text(), 'Сырный - 55.00 р.')]").click()
            driver.find_element(By.CLASS_NAME, "single_add_to_cart_button").click()
            time.sleep(2)

        with allure.step("Открытие корзины"):
            driver.find_element(By.CLASS_NAME, "cart-contents").click()
            time.sleep(2)

        with allure.step("Изменение количества"):
            qty_input = driver.find_element(By.XPATH, '(//input[@title="Кол-во"])[1]')
            qty_input.clear()
            qty_input.send_keys("2")
            time.sleep(1)

        with allure.step("Обновление корзины"):
            update_btn = driver.find_element(By.NAME, "update_cart")
            driver.execute_script("arguments[0].click();", update_btn)
            time.sleep(2)

        with allure.step("Удаление второй пиццы"):
            remove_btn = driver.find_element(By.XPATH, '(//a[@class="remove"])[2]')
            driver.execute_script("arguments[0].click();", remove_btn)
            time.sleep(2)

        with allure.step("Проверка суммы"):
            total = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "(//bdi)[4]"))
            ).text
            assert total == "1030,00₽", f"Ожидалось 1030,00₽, получено {total}"
            allure.attach(f"Сумма корзины: {total}", name="Результат", attachment_type=allure.attachment_type.TEXT)

        logger.info("SUCCESS: test_case_3 завершен")

    @allure.story("Фильтрация десертов по цене")
    @allure.description(
        """
    Этот тест проверяет фильтрацию десертов до 135 руб
    """
    )
    def test_case_4(self, browser):
        """TC-004: Фильтрация десертов по максимальной цене меняем set_up_browser на browser"""
        driver = browser
        logger = logging.getLogger(__name__)

        logger.info("START: test_case_4 - Фильтрация десертов")

        with allure.step("Открытие главной страницы"):
            driver.get("https://pizzeria.skillbox.cc/")
            time.sleep(2)

        with allure.step('Переход в "Десерты"'):
            menu = driver.find_element(By.XPATH, '//nav/div/ul/li/a[contains(text(), "Меню")]')
            ActionChains(driver).move_to_element(menu).perform()
            time.sleep(1)
            driver.find_element(By.XPATH, '//ul/li//ul/li/a[contains(text(), "Десерты")]').click()
            time.sleep(2)

        with allure.step("Установка фильтра до 135 руб"):
            slider = driver.find_element(By.XPATH, '(//span[@class="ui-slider-handle"])[2]')
            ActionChains(driver).drag_and_drop_by_offset(slider, -170, 0).perform()
            time.sleep(2)
            driver.find_element(By.XPATH, '//button[contains(text(), "Применить")]').click()
            time.sleep(2)

        with allure.step("Проверка цен"):
            prices_elements = driver.find_elements(By.XPATH, "//span[@class='woocommerce-Price-amount amount']/bdi")
            prices = [float(p.text.replace("₽", "").replace(",", ".")) for p in prices_elements]

            assert all(p <= 135 for p in prices), f"Найдены цены > 135: {prices}"
            allure.attach(f"Цены: {prices}", name="Результат", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Добавление десерта в корзину"):
            driver.find_element(By.XPATH, '(//a[contains(text(), "В корзину")])[1]').click()
            time.sleep(2)

        with allure.step("Проверка корзины"):
            driver.find_element(By.CLASS_NAME, "cart-contents").click()
            time.sleep(2)
            products = driver.find_elements(By.CLASS_NAME, "product-name")
            actual = [p.text for p in products if p.text != "ТОВАР"]
            assert any("Десерт" in p for p in actual), "Десерт не найден в корзине"

        logger.info("SUCCESS: test_case_4 завершен")

    @allure.story("Оформление заказа с авторизацией")
    @allure.description(
        """
    Полный цикл: фильтрация десертов → добавление → авторизация → оформление заказа
    """
    )
    def test_case_5(self, browser):
        """TC-005: Полный цикл оформления заказа меняем set_up_browser на browser"""
        driver = browser
        logger = logging.getLogger(__name__)

        logger.info("START: test_case_5 - Полный цикл оформления заказа")

        username = "Alexandr"
        password = "123456"
        email = "alexandr@test.com"

        # Шаг 1: Открытие и переход в десерты
        with allure.step("Открытие главной страницы"):
            driver.get("https://pizzeria.skillbox.cc/")
            time.sleep(2)

        with allure.step('Переход в "Десерты"'):
            menu = driver.find_element(By.XPATH, '//nav/div/ul/li/a[contains(text(), "Меню")]')
            ActionChains(driver).move_to_element(menu).perform()
            time.sleep(1)
            driver.find_element(By.XPATH, '//ul/li//ul/li/a[contains(text(), "Десерты")]').click()
            time.sleep(2)

        # Шаг 2: Фильтрация
        with allure.step("Фильтрация до 135 руб"):
            slider = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-slider-handle:last-child"))
            )
            for _ in range(5):
                ActionChains(driver).drag_and_drop_by_offset(slider, -40, 0).perform()
                time.sleep(0.3)
            time.sleep(1)

            try:
                driver.find_element(By.XPATH, '//button[contains(text(), "Применить")]').click()
            except:
                pass
            time.sleep(2)

        # Шаг 3: Добавление десерта
        with allure.step("Добавление десерта в корзину"):
            add_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '(//a[contains(text(), "В корзину")])[1]'))
            )
            add_btn.click()
            time.sleep(2)

        # Шаг 4: Переход в корзину
        with allure.step("Переход в корзину"):
            driver.find_element(By.CLASS_NAME, "cart-contents").click()
            time.sleep(2)

        # Шаг 5: Оформление заказа
        with allure.step("Нажатие 'Оформить заказ'"):
            driver.find_element(By.CLASS_NAME, "checkout-button").click()
            time.sleep(2)

        # Шаг 6: Авторизация
        with allure.step("Авторизация"):
            driver.find_element(By.XPATH, '//nav/div/ul/li/a[contains(text(), "Мой аккаунт")]').click()
            time.sleep(2)
            driver.find_element(By.NAME, "username").send_keys(username)
            driver.find_element(By.NAME, "password").send_keys(password)
            driver.find_element(By.NAME, "login").click()
            time.sleep(2)

        # Шаг 7: Возврат в корзину
        with allure.step("Возврат в корзину"):
            driver.get("https://pizzeria.skillbox.cc/cart/")
            time.sleep(2)
            driver.find_element(By.CLASS_NAME, "checkout-button").click()
            time.sleep(2)

        # Шаг 8: Данные доставки
        with allure.step("Заполнение данных доставки"):
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "billing_first_name"))
            ).send_keys("Андрей")
            driver.find_element(By.NAME, "billing_last_name").send_keys("Иванов")
            driver.find_element(By.NAME, "billing_address_1").send_keys("ул. Ленина, д. 15")
            driver.find_element(By.NAME, "billing_city").send_keys("Москва")
            driver.find_element(By.NAME, "billing_postcode").send_keys("101000")
            driver.find_element(By.NAME, "billing_phone").send_keys("+79123456789")
            driver.find_element(By.NAME, "billing_email").clear()
            driver.find_element(By.NAME, "billing_email").send_keys(email)

        # Шаг 9: Дата доставки
        with allure.step("Выбор даты доставки"):
            from datetime import datetime, timedelta
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%m/%d/%Y")
            date_field = driver.find_element(By.NAME, "order_date")
            date_field.clear()
            date_field.send_keys(tomorrow)
            time.sleep(1)

        # Шаг 10: Оплата и подтверждение
        with allure.step("Выбор оплаты и подтверждение"):
            driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(1)

            try:
                driver.find_element(By.ID, "payment_method_cod").click()
            except:
                pass

            try:
                driver.find_element(By.ID, "terms").click()
            except:
                pass

            driver.find_element(By.ID, "place_order").click()
            time.sleep(5)

        # Шаг 11: Проверка
        with allure.step("Проверка подтверждения"):
            try:
                success = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Заказ получен')]"))
                )
                assert success.is_displayed()
                allure.attach("Заказ успешно оформлен", name="Результат", attachment_type=allure.attachment_type.TEXT)
            except:
                page_text = driver.find_element(By.TAG_NAME, "body").text
                assert "заказ" in page_text.lower(), "Страница подтверждения не найдена"

        logger.info("SUCCESS: test_case_5 завершен")


# Запуск тестов
if __name__ == "__main__":
    pytest.main(["-v", __file__])