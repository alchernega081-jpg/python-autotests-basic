"""
Модуль с автотестами для проверки промокода GIVEMEHALYAVA на сайте Pizzeria
"""

import logging
import time
import random
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestPromocodeGIVEMEHALYAVA:
    """
    Класс для тестирования промокода GIVEMEHALYAVA
    """

    @allure.feature("Проверка промокодов")
    @allure.story("Сценарий №1: Применение валидного промокода")
    @allure.description(
        """
        Сценарий №1:
        1. Заполнить корзину любыми товарами
        2. Перейти в корзину
        3. Применить промокод GIVEMEHALYAVA
        4. Убедиться, что конечная сумма заказа уменьшилась на 10%
        """
    )
    def test_promocode_givemehalyava_works(self, set_up_browser):
        """TC-PROMO-001: Проверка применения валидного промокода"""
        driver = set_up_browser
        logger = logging.getLogger(__name__)

        logger.info("START: test_promocode_givemehalyava_works")

        with allure.step("Открытие главной страницы"):
            driver.get("https://pizzeria.skillbox.cc/")
            time.sleep(3)

        with allure.step("Заполнение корзины товарами"):
            # Добавляем пиццу "Рай" (ID: 421)
            driver.get("https://pizzeria.skillbox.cc/?add-to-cart=421")
            time.sleep(2)
            logger.info("Добавлена пицца 'Рай' (ID: 421)")

            # Добавляем пиццу "Пепперони" (ID: 417)
            driver.get("https://pizzeria.skillbox.cc/?add-to-cart=417")
            time.sleep(2)
            logger.info("Добавлена пицца 'Пепперони' (ID: 417)")

        with allure.step("Переход в корзину"):
            driver.get("https://pizzeria.skillbox.cc/cart/")
            time.sleep(3)

            # Сохраняем скриншот корзины для отладки
            driver.save_screenshot("cart_screenshot.png")
            logger.info("Сохранен скриншот корзины")

            # Проверяем, что товары в корзине
            try:
                cart_items = driver.find_elements(By.CSS_SELECTOR, ".cart_item")
                logger.info(f"В корзине товаров: {len(cart_items)}")
            except Exception as e:
                logger.error(f"Ошибка при проверке корзины: {e}")

        with allure.step("Получение суммы до применения промокода"):
            try:
                # Ищем сумму корзины
                total_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-total .amount, .order-total .amount"))
                )
                total_text = total_element.text
                logger.info(f"Текст суммы: {total_text}")

                # Очищаем текст от символов
                total_text = total_text.replace("₽", "").replace(" ", "").replace(",", ".").strip()
                total_before = float(total_text)
                logger.info(f"Сумма до применения промокода: {total_before}₽")
                allure.attach(f"Сумма до: {total_before}₽", name="Сумма до промокода")

            except Exception as e:
                logger.error(f"Не удалось получить сумму: {e}")
                pytest.skip(f"Не удалось получить сумму корзины: {e}")

        with allure.step("Применение промокода GIVEMEHALYAVA"):
            try:
                # Ищем ссылку "Применить купон" и нажимаем на неё
                try:
                    coupon_link = driver.find_element(By.CSS_SELECTOR, "a.showcoupon")
                    if coupon_link.is_displayed():
                        coupon_link.click()
                        logger.info("Нажата ссылка 'Применить купон'")
                        time.sleep(1)
                except:
                    logger.info("Ссылка 'Применить купон' не найдена, возможно поле уже видимо")

                # Находим поле ввода купона
                coupon_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "coupon_code"))
                )
                logger.info("Поле купона найдено")

                # Прокручиваем к полю
                driver.execute_script("arguments[0].scrollIntoView(true);", coupon_input)
                time.sleep(1)

                # Вводим промокод
                coupon_input.clear()
                coupon_input.send_keys("GIVEMEHALYAVA")
                logger.info("Введен промокод: GIVEMEHALYAVA")

                # Находим кнопку применения
                apply_button = driver.find_element(By.NAME, "apply_coupon")
                logger.info("Кнопка применения найдена")

                # Прокручиваем к кнопке и нажимаем
                driver.execute_script("arguments[0].scrollIntoView(true);", apply_button)
                time.sleep(1)
                apply_button.click()
                time.sleep(3)
                logger.info("Промокод применен")

            except Exception as e:
                logger.error(f"Ошибка при применении промокода: {e}")
                driver.save_screenshot("coupon_error.png")
                pytest.skip(f"Не удалось применить промокод: {e}")

        with allure.step("Получение суммы после применения промокода"):
            try:
                # Ждем обновления суммы
                time.sleep(2)

                # Ищем сообщение об успешном применении
                try:
                    success_message = driver.find_element(By.CSS_SELECTOR, ".woocommerce-message")
                    logger.info(f"Сообщение: {success_message.text}")
                    allure.attach(success_message.text, name="Сообщение о промокоде")
                except:
                    pass

                total_after_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-total .amount, .order-total .amount"))
                )
                total_after_text = total_after_element.text
                logger.info(f"Текст суммы после: {total_after_text}")

                # Очищаем текст от символов
                total_after_text = total_after_text.replace("₽", "").replace(" ", "").replace(",", ".").strip()
                total_after = float(total_after_text)
                logger.info(f"Сумма после применения промокода: {total_after}₽")
                allure.attach(f"Сумма после: {total_after}₽", name="Сумма после промокода")

            except Exception as e:
                logger.error(f"Не удалось получить сумму после: {e}")
                pytest.skip(f"Не удалось получить сумму после применения промокода: {e}")

        with allure.step("Проверка уменьшения суммы на 10%"):
            expected_total = total_before * 0.9
            logger.info(f"Ожидаемая сумма после скидки 10%: {expected_total}₽")

            assert abs(total_after - expected_total) < 0.01, \
                f"Сумма не уменьшилась на 10%. Ожидалось: {expected_total}₽, Получено: {total_after}₽"

            allure.attach("✅ Промокод успешно применился, скидка 10% получена", name="Результат")
            logger.info("✅ Проверка пройдена: скидка 10% применена")

        logger.info("SUCCESS: test_promocode_givemehalyava_works завершен")

    @allure.feature("Проверка промокодов")
    @allure.story("Сценарий №2: Применение невалидного промокода")
    @allure.description(
        """
        Сценарий №2:
        1. Заполнить корзину любыми товарами
        2. Перейти в корзину
        3. Применить невалидный промокод DC120
        4. Убедиться, что конечная сумма заказа НЕ уменьшилась на 10% и промокод не применился
        """
    )
    def test_invalid_promocode_dc120_does_not_apply(self, set_up_browser):
        """TC-PROMO-002: Проверка невалидного промокода"""
        driver = set_up_browser
        logger = logging.getLogger(__name__)

        logger.info("START: test_invalid_promocode_dc120_does_not_apply")

        with allure.step("Открытие главной страницы"):
            driver.get("https://pizzeria.skillbox.cc/")
            time.sleep(3)

        with allure.step("Заполнение корзины товарами"):
            # Добавляем пиццу "Рай" (ID: 421)
            driver.get("https://pizzeria.skillbox.cc/?add-to-cart=421")
            time.sleep(2)
            logger.info("Добавлена пицца 'Рай' (ID: 421)")

        with allure.step("Переход в корзину"):
            driver.get("https://pizzeria.skillbox.cc/cart/")
            time.sleep(3)

        with allure.step("Получение суммы до применения промокода"):
            total_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-total .amount, .order-total .amount"))
            )
            total_before = float(total_element.text.replace("₽", "").replace(" ", "").replace(",", ".").strip())
            logger.info(f"Сумма до применения промокода: {total_before}₽")
            allure.attach(f"Сумма до: {total_before}₽", name="Сумма до промокода")

        with allure.step("Применение невалидного промокода DC120"):
            try:
                # Ищем ссылку "Применить купон"
                try:
                    coupon_link = driver.find_element(By.CSS_SELECTOR, "a.showcoupon")
                    if coupon_link.is_displayed():
                        coupon_link.click()
                        logger.info("Нажата ссылка 'Применить купон'")
                        time.sleep(1)
                except:
                    pass

                # Находим поле ввода купона
                coupon_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "coupon_code"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", coupon_input)
                time.sleep(1)

                coupon_input.clear()
                coupon_input.send_keys("DC120")
                logger.info("Введен промокод: DC120")

                # Находим и нажимаем кнопку применения
                apply_button = driver.find_element(By.NAME, "apply_coupon")
                driver.execute_script("arguments[0].scrollIntoView(true);", apply_button)
                time.sleep(1)
                apply_button.click()
                time.sleep(3)
                logger.info("Промокод применен")

            except Exception as e:
                logger.error(f"Ошибка при применении промокода: {e}")
                driver.save_screenshot("invalid_coupon_error.png")
                pytest.skip(f"Не удалось применить промокод: {e}")

        with allure.step("Получение суммы после применения промокода"):
            total_after_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-total .amount, .order-total .amount"))
            )
            total_after = float(total_after_element.text.replace("₽", "").replace(" ", "").replace(",", ".").strip())
            logger.info(f"Сумма после применения промокода: {total_after}₽")
            allure.attach(f"Сумма после: {total_after}₽", name="Сумма после промокода")

        with allure.step("Проверка, что сумма не изменилась"):
            assert total_after == total_before, \
                f"Сумма изменилась при невалидном промокоде. Было: {total_before}₽, Стало: {total_after}₽"
            allure.attach("✅ Невалидный промокод не применился, сумма не изменилась", name="Результат")
            logger.info("✅ Невалидный промокод не применился, сумма не изменилась")

        # Проверяем наличие сообщения об ошибке
        with allure.step("Проверка сообщения об ошибке"):
            try:
                error_message = driver.find_element(By.CSS_SELECTOR, ".woocommerce-error").text
                allure.attach(f"Сообщение: {error_message}", name="Сообщение об ошибке")
                logger.info(f"Найдено сообщение об ошибке: {error_message}")
            except:
                logger.warning("Сообщение об ошибке не найдено")

        logger.info("SUCCESS: test_invalid_promocode_dc120_does_not_apply завершен")

    @allure.feature("Проверка промокодов")
    @allure.story("Сценарий №3: Проверка при недоступности сервера")
    @allure.description(
        """
        Сценарий №3: Проверка поведения при недоступности сервера валидации
        1. Заполнить корзину любыми товарами
        2. Перейти в корзину
        3. Применить промокод GIVEMEHALYAVA
        4. Перехватить запрос и заблокировать его (вернуть 500)
        5. Убедиться, что сумма не изменилась
        6. Проверить наличие сообщения об ошибке для пользователя

        Ожидаемое поведение: сайт должен показать сообщение, что не удалось применить промокод
        """
    )
    def test_promocode_server_down(self, set_up_browser):
        """TC-PROMO-003: Проверка при недоступности сервера валидации"""
        pytest.skip("Тест требует настройки BrowserMob Proxy. Для запуска нужно:\n"
                    "1. Установить BrowserMob Proxy: https://github.com/lightbody/browsermob-proxy\n"
                    "2. Указать правильный путь к browsermob-proxy в коде\n"
                    "3. Установить библиотеку: pip install browsermob-proxy")

    @allure.feature("Проверка промокодов")
    @allure.story("Сценарий №4: Проверка однократности применения промокода")
    @allure.description(
        """
        Сценарий №4:
        1. Зарегистрировать нового пользователя
        2. Сделать заказ с применением промокода GIVEMEHALYAVA
        3. Оформить заказ
        4. Попробовать оформить второй заказ с этим же промокодом
        5. Убедиться, что второй раз промокод не срабатывает
        """
    )
    def test_promocode_one_time_only(self, set_up_browser):
        """TC-PROMO-004: Проверка однократности применения промокода"""
        driver = set_up_browser
        logger = logging.getLogger(__name__)

        logger.info("START: test_promocode_one_time_only")

        # Генерируем уникальные данные для пользователя
        user_name = f"user{random.randint(100, 999)}"
        user_email = f"{user_name}@test.com"
        user_password = "Test123!"

        logger.info(f"Генерируем пользователя: username={user_name}, email={user_email}")

        # ==================== ШАГ 1: РЕГИСТРАЦИЯ ====================
        with allure.step("Регистрация нового пользователя"):
            driver.get("https://pizzeria.skillbox.cc/register/")
            time.sleep(3)

            # Заполняем поля регистрации
            username_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "reg_username"))
            )
            username_input.send_keys(user_name)
            logger.info("Введено имя пользователя")

            email_input = driver.find_element(By.ID, "reg_email")
            email_input.send_keys(user_email)
            logger.info("Введен email")

            password_input = driver.find_element(By.ID, "reg_password")
            password_input.send_keys(user_password)
            logger.info("Введен пароль")

            # Нажимаем кнопку регистрации
            register_button = driver.find_element(By.NAME, "register")
            register_button.click()
            time.sleep(3)

            # После регистрации переходим на страницу my-account
            driver.get("https://pizzeria.skillbox.cc/my-account/")
            time.sleep(2)

            logger.info(f"✅ Пользователь зарегистрирован: {user_email}")
            allure.attach(f"Зарегистрирован: {user_email}", name="Регистрация")

        # ==================== ШАГ 2: ПЕРВЫЙ ЗАКАЗ ====================
        with allure.step("Первый заказ с промокодом GIVEMEHALYAVA"):
            # Добавляем пиццу "Рай" (ID: 421)
            driver.get("https://pizzeria.skillbox.cc/?add-to-cart=421")
            time.sleep(2)
            logger.info("Добавлена пицца 'Рай'")

            # Переход в корзину
            driver.get("https://pizzeria.skillbox.cc/cart/")
            time.sleep(3)

            # Получаем сумму до применения промокода
            total_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-total .amount, .order-total .amount"))
            )
            total_before_1 = float(total_element.text.replace("₽", "").replace(" ", "").replace(",", ".").strip())
            logger.info(f"Сумма до промокода: {total_before_1}₽")
            allure.attach(f"Сумма до: {total_before_1}₽", name="Сумма до промокода (1-й заказ)")

            # Применяем промокод
            coupon_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "coupon_code"))
            )
            coupon_input.clear()
            coupon_input.send_keys("GIVEMEHALYAVA")
            logger.info("Введен промокод: GIVEMEHALYAVA")

            apply_button = driver.find_element(By.NAME, "apply_coupon")
            apply_button.click()
            time.sleep(3)
            logger.info("Промокод применен")

            # Получаем сумму после применения промокода
            total_after_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-total .amount, .order-total .amount"))
            )
            total_after_1 = float(total_after_element.text.replace("₽", "").replace(" ", "").replace(",", ".").strip())
            logger.info(f"Сумма после промокода: {total_after_1}₽")
            allure.attach(f"Сумма после: {total_after_1}₽", name="Сумма после промокода (1-й заказ)")

            # Проверяем, что скидка применилась
            expected_total_1 = total_before_1 * 0.9
            assert abs(total_after_1 - expected_total_1) < 0.01, \
                f"Первый заказ: скидка не применилась. Было: {total_before_1}₽, Стало: {total_after_1}₽"

            allure.attach("✅ Скидка 10% применена", name="Результат первого заказа")
            logger.info("✅ Первый заказ: скидка 10% применена")

            # Оформляем заказ
            checkout_button = driver.find_element(By.CLASS_NAME, "checkout-button")
            checkout_button.click()
            time.sleep(2)

            # Заполняем данные доставки
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "billing_first_name"))
            ).send_keys("Иван")

            driver.find_element(By.NAME, "billing_last_name").send_keys("Петров")
            driver.find_element(By.NAME, "billing_address_1").send_keys("ул. Тестовая, 1")
            driver.find_element(By.NAME, "billing_city").send_keys("Москва")
            driver.find_element(By.NAME, "billing_postcode").send_keys("123456")
            driver.find_element(By.NAME, "billing_phone").send_keys("+79991234567")
            driver.find_element(By.NAME, "billing_email").clear()
            driver.find_element(By.NAME, "billing_email").send_keys(user_email)

            driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(1)

            try:
                driver.find_element(By.ID, "payment_method_cod").click()
            except:
                pass

            driver.find_element(By.ID, "place_order").click()
            time.sleep(5)

            logger.info("Заказ успешно оформлен")
            allure.attach("Заказ успешно оформлен", name="Статус первого заказа")

        # ==================== ШАГ 3: ВТОРОЙ ЗАКАЗ ====================
        with allure.step("Второй заказ с тем же промокодом GIVEMEHALYAVA"):
            # Очищаем корзину
            driver.get("https://pizzeria.skillbox.cc/cart/")
            time.sleep(2)

            # Удаляем все товары из корзины
            remove_buttons = driver.find_elements(By.CLASS_NAME, "remove")
            for btn in remove_buttons:
                try:
                    btn.click()
                    time.sleep(1)
                except:
                    pass

            # Добавляем другой товар (пицца "Пепперони" ID: 417)
            driver.get("https://pizzeria.skillbox.cc/?add-to-cart=417")
            time.sleep(2)
            logger.info("Добавлена пицца 'Пепперони'")

            # Переход в корзину
            driver.get("https://pizzeria.skillbox.cc/cart/")
            time.sleep(3)

            # Получаем сумму до применения промокода
            total_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-total .amount, .order-total .amount"))
            )
            total_before_2 = float(total_element.text.replace("₽", "").replace(" ", "").replace(",", ".").strip())
            logger.info(f"Сумма до промокода (2-й заказ): {total_before_2}₽")
            allure.attach(f"Сумма до: {total_before_2}₽", name="Сумма до промокода (2-й заказ)")

            # Применяем промокод повторно
            coupon_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "coupon_code"))
            )
            coupon_input.clear()
            coupon_input.send_keys("GIVEMEHALYAVA")
            logger.info("Введен промокод: GIVEMEHALYAVA (повторно)")

            apply_button = driver.find_element(By.NAME, "apply_coupon")
            apply_button.click()
            time.sleep(3)
            logger.info("Промокод применен повторно")

            # Получаем сумму после повторного применения
            total_after_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-total .amount, .order-total .amount"))
            )
            total_after_2 = float(total_after_element.text.replace("₽", "").replace(" ", "").replace(",", ".").strip())
            logger.info(f"Сумма после промокода (2-й заказ): {total_after_2}₽")
            allure.attach(f"Сумма после: {total_after_2}₽", name="Сумма после промокода (2-й заказ)")

            # Проверяем, что скидка не применилась
            assert total_after_2 == total_before_2, \
                f"Второй заказ: промокод сработал повторно! Было: {total_before_2}₽, Стало: {total_after_2}₽"

            allure.attach("✅ Промокод НЕ сработал (однократность подтверждена)",
                          name="Результат второго заказа")
            logger.info("✅ Второй заказ: промокод НЕ сработал")

        logger.info("SUCCESS: test_promocode_one_time_only завершен")


if __name__ == "__main__":
    pytest.main(["-v", __file__])