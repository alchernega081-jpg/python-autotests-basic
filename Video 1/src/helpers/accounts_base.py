import allure
import pytest
import logging

# Создаем логгер для этого модуля
logger = logging.getLogger('request')


class AccountsBase:

    @pytest.fixture()
    def go_to_github(self, selenium):
        with allure.step('Открытие страницы http://github.com'):
            url = 'http://github.com'
            # Логирование действия
            logger.info(f"Navigating to URL: {url}")
            selenium.get(url)
            logger.info(f"Successfully loaded page: {url}")
            return selenium