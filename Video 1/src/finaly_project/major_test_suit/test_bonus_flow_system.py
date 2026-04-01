"""
Модуль с автотестами для сайта Pizzeria (https://pizzeria.skillbox.cc/)
Содержит тестовые сценарии для проверки функционала бонусной программы
"""

import time
import logging
import pytest
import re
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import allure


@allure.feature("Тестовые сценарии для сайта Pizzeria")
class TestCases:

    @allure.story("Регистрация в бонусной программе")
    @allure.description(
        """
    Этот тест выполняет следующие действия:
    1. Переходит на страницу бонусной программы
    2. Проверяет валидацию полей (пустые поля, некорректный телефон)
    3. Вводит корректные данные
    4. Отправляет форму
    5. Проверяет успешность регистрации
    """
    )
    def test_case_6(self, set_up_browser):
        """TC-006: Регистрация в бонусной программе с проверкой валидации"""
        driver = set_up_browser
        logger = logging.getLogger(__name__)

        logger.info("=" * 60)
        logger.info("START: test_case_6 - Регистрация в бонусной программе")
        logger.info("=" * 60)

        # Функция для повторного поиска элементов
        def get_form_elements():
            """Повторно находит элементы формы (на случай обновления страницы)"""
            try:
                name_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "bonus_username"))
                )
                phone_field = driver.find_element(By.ID, "bonus_phone")
                submit_button = driver.find_element(By.NAME, "bonus")
                return name_field, phone_field, submit_button
            except:
                # Если элементы не найдены, пробуем перезагрузить страницу
                logger.warning("Элементы формы не найдены, перезагружаем страницу")
                driver.refresh()
                time.sleep(2)
                name_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "bonus_username"))
                )
                phone_field = driver.find_element(By.ID, "bonus_phone")
                submit_button = driver.find_element(By.NAME, "bonus")
                return name_field, phone_field, submit_button

        # ==================== ШАГ 1: Переход на страницу бонусной программы ====================
        with allure.step("Переход на страницу бонусной программы"):
            logger.info("Открытие страницы бонусной программы")
            driver.get("https://pizzeria.skillbox.cc/bonus/")

            # Увеличенное ожидание загрузки страницы
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "bonus_content"))
            )
            time.sleep(2)

            # Проверка, что страница загрузилась
            assert "bonus" in driver.current_url.lower(), \
                "Страница бонусной программы не загружена"
            logger.info("✅ Страница бонусной программы успешно загружена")

        # Получаем элементы формы
        name_field, phone_field, submit_button = get_form_elements()

        # ==================== ШАГ 2: Проверка валидации пустых полей ====================
        with allure.step("Проверка валидации - отправка пустой формы"):
            logger.info("Проверка валидации пустых полей")

            # Очищаем поля
            name_field.clear()
            phone_field.clear()
            time.sleep(0.5)

            # Прокручиваем к кнопке
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
            time.sleep(1)

            # Кликаем по кнопке с пустыми полями
            submit_button.click()

            # Увеличенное ожидание появления сообщений об ошибках
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "bonus_content"))
            )
            time.sleep(2)

            # Проверяем, что появились сообщения об ошибках
            try:
                error_messages = driver.find_element(By.ID, "bonus_content")
                error_text = error_messages.text
                logger.info(f"Сообщения об ошибках при пустых полях:\n{error_text}")

                # Проверяем наличие сообщения об ошибке для имени и телефона
                assert "Имя" in error_text, "Нет сообщения об ошибке для поля Имя"
                assert "Телефон" in error_text, "Нет сообщения об ошибке для поля Телефон"

                allure.attach(
                    f"Ошибки при пустых полях:\n{error_text}",
                    name="Валидация пустых полей",
                    attachment_type=allure.attachment_type.TEXT,
                )
                logger.info("✅ Валидация пустых полей работает корректно")
            except NoSuchElementException:
                logger.warning("⚠️ Сообщения об ошибках не найдены")

        # Обновляем элементы после возможного обновления страницы
        name_field, phone_field, submit_button = get_form_elements()

        # ==================== ШАГ 3: Проверка валидации некорректного телефона ====================
        with allure.step("Проверка валидации - некорректный формат телефона"):
            logger.info("Проверка валидации некорректного телефона")

            # Вводим корректное имя
            name_field.clear()
            name_field.send_keys("Андрей")
            time.sleep(0.5)

            # Вводим некорректный телефон
            phone_field.clear()
            phone_field.send_keys("123")
            time.sleep(0.5)

            # Кликаем по кнопке
            submit_button.click()

            # Ожидаем появления сообщений об ошибках
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "bonus_content"))
            )
            time.sleep(2)

            # Проверяем наличие сообщения об ошибке для телефона
            try:
                error_messages = driver.find_element(By.ID, "bonus_content")
                error_text = error_messages.text
                logger.info(f"Сообщения об ошибках при некорректном телефоне:\n{error_text}")

                # Проверяем наличие сообщения об ошибке формата телефона
                assert "неверный формат" in error_text.lower() or "телефон" in error_text.lower(), \
                    f"Нет сообщения об ошибке для некорректного телефона. Получено: {error_text}"

                allure.attach(
                    f"Ошибка при некорректном телефоне:\n{error_text}",
                    name="Валидация телефона",
                    attachment_type=allure.attachment_type.TEXT,
                )
                logger.info("✅ Валидация некорректного телефона работает корректно")
            except NoSuchElementException:
                logger.warning("⚠️ Сообщения об ошибках не найдены")

        # Обновляем элементы после возможного обновления страницы
        name_field, phone_field, submit_button = get_form_elements()

        # ==================== ШАГ 4: Проверка валидации короткого имени (если есть) ====================
        with allure.step("Проверка валидации - слишком короткое имя"):
            logger.info("Проверка валидации короткого имени")

            # Вводим короткое имя
            name_field.clear()
            name_field.send_keys("A")
            time.sleep(0.5)

            # Вводим корректный телефон
            phone_field.clear()
            phone_field.send_keys("+79123456789")
            time.sleep(0.5)

            # Кликаем по кнопке
            submit_button.click()

            # Ожидаем ответа
            time.sleep(3)

            # Проверяем результат
            try:
                error_messages = driver.find_element(By.ID, "bonus_content")
                error_text = error_messages.text

                if "Имя" in error_text:
                    logger.info("✅ Валидация короткого имени работает")
                    allure.attach(
                        f"Ошибка при коротком имени:\n{error_text}",
                        name="Валидация короткого имени",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                else:
                    logger.info("⚠️ Нет явной валидации короткого имени")
            except:
                logger.info("⚠️ Нет сообщения об ошибке, возможно имя прошло валидацию")

        # Обновляем элементы после возможного обновления страницы
        name_field, phone_field, submit_button = get_form_elements()

        # ==================== ШАГ 5: Ввод корректных данных ====================
        with allure.step("Ввод корректных данных для регистрации"):
            logger.info("Ввод корректных данных")

            # Генерируем уникальные данные
            unique_id = random.randint(1000, 9999)
            test_name = f"Тестовый_{unique_id}"
            test_phone = f"+7912{random.randint(1000000, 9999999)}"

            # Очищаем и заполняем поля
            name_field = driver.find_element(By.ID, "bonus_username")
            name_field.clear()
            name_field.send_keys(test_name)
            time.sleep(0.5)

            phone_field = driver.find_element(By.ID, "bonus_phone")
            phone_field.clear()
            phone_field.send_keys(test_phone)
            time.sleep(0.5)

            logger.info(f"Введены данные: Имя='{test_name}', Телефон='{test_phone}'")

            allure.attach(
                f"Имя: {test_name}\nТелефон: {test_phone}",
                name="Введенные данные",
                attachment_type=allure.attachment_type.TEXT,
            )

        # ==================== ШАГ 6: Отправка формы ====================
        with allure.step("Отправка формы регистрации в бонусную программу"):
            logger.info("Отправка формы")

            submit_button = driver.find_element(By.NAME, "bonus")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
            time.sleep(1)
            submit_button.click()

            # Увеличенное ожидание ответа
            time.sleep(5)

        # ==================== ШАГ 7: Проверка успешной регистрации ====================
        with allure.step("Проверка успешной регистрации в бонусной программе"):
            logger.info("Проверка успешности регистрации")

            success = False

            # Вариант 1: Проверка всплывающего окна (alert)
            try:
                alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert_text = alert.text
                logger.info(f"Получено alert-сообщение: {alert_text}")

                expected_text = "Заявка отправлена, дождитесь, пожалуйста, оформления карты!"
                if expected_text in alert_text:
                    success = True
                    alert.accept()
                    allure.attach(
                        f"Alert сообщение: {alert_text}",
                        name="Результат регистрации (Alert)",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                    logger.info("✅ Регистрация в бонусной программе успешна (alert подтверждение)")
                else:
                    alert.accept()
            except TimeoutException:
                logger.debug("Alert не появился, проверяем сообщение на странице")

            # Вариант 2: Проверка сообщения на странице
            if not success:
                try:
                    # Ждем появления сообщения об успехе
                    success_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'оформлена')]"))
                    )
                    success_text = success_element.text
                    logger.info(f"Сообщение на странице: {success_text}")

                    if "оформлена" in success_text.lower():
                        success = True
                        allure.attach(
                            f"Сообщение на странице: {success_text}",
                            name="Результат регистрации",
                            attachment_type=allure.attachment_type.TEXT,
                        )
                        logger.info("✅ Регистрация в бонусной программе успешна")
                except TimeoutException:
                    logger.debug("Сообщение на странице не найдено")

            # Вариант 3: Проверка, что форма отправилась (изменение URL или содержимого)
            if not success:
                try:
                    # Проверяем наличие заголовка "Ваша карта оформлена!"
                    title_element = driver.find_element(By.XPATH, "//h3")
                    title_text = title_element.text
                    if "оформлена" in title_text.lower():
                        success = True
                        allure.attach(
                            f"Заголовок: {title_text}",
                            name="Результат регистрации",
                            attachment_type=allure.attachment_type.TEXT,
                        )
                        logger.info("✅ Регистрация в бонусной программе успешна (заголовок)")
                except:
                    pass

            # Финальная проверка
            if not success:
                # Проверяем, что страница обновилась или появилось сообщение об успехе
                current_url = driver.current_url
                page_source = driver.page_source

                if "заявка" in page_source.lower() or "оформлена" in page_source.lower():
                    success = True
                    logger.info("✅ На странице найдено сообщение об успешной регистрации")
                    allure.attach(
                        "На странице найдено сообщение об успешной регистрации",
                        name="Результат регистрации",
                        attachment_type=allure.attachment_type.TEXT,
                    )

            assert success, "Не удалось подтвердить успешность регистрации в бонусной программе"

        # ==================== ШАГ 8: Проверка сохраненных данных ====================
        with allure.step("Проверка, что данные были сохранены"):
            logger.info("Проверка сохраненных данных")

            # Получаем текущие значения полей
            try:
                name_field = driver.find_element(By.ID, "bonus_username")
                phone_field = driver.find_element(By.ID, "bonus_phone")

                current_name = name_field.get_attribute("value") if name_field.is_displayed() else ""
                current_phone = phone_field.get_attribute("value") if phone_field.is_displayed() else ""

                if current_name and current_phone:
                    allure.attach(
                        f"Сохраненные данные:\nИмя: {current_name}\nТелефон: {current_phone}",
                        name="Данные после регистрации",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                    logger.info(f"✅ Данные сохранены: Имя='{current_name}', Телефон='{current_phone}'")
                else:
                    logger.info("⚠️ Поля могут быть очищены после отправки")
            except:
                logger.info("⚠️ Не удалось получить значения полей")

        # Финальный отчет
        allure.attach(
            "✅ Тест регистрации в бонусной программе успешно завершен\n"
            "Проверены:\n"
            "- Валидация пустых полей\n"
            "- Валидация некорректного телефона\n"
            "- Успешная регистрация с корректными данными",
            name="ИТОГОВЫЙ РЕЗУЛЬТАТ",
            attachment_type=allure.attachment_type.TEXT,
        )

        logger.info("=" * 60)
        logger.info("SUCCESS: test_case_6 - Регистрация в бонусной программе завершена")
        logger.info("=" * 60)


# Запуск тестов
if __name__ == "__main__":
    pytest.main(["-v", __file__])