import os
import logging
import logging.config
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Настройка логирования
def setup_logging():
    """Инициализация логирования из конфигурационного файла"""
    config_file = os.path.join(os.path.dirname(__file__), "logging.ini")
    if os.path.exists(config_file):
        logging.config.fileConfig(config_file)
    else:
        # Базовая конфигурация, если файл не найден
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s][%(levelname)s][%(name)s][%(filename)s:%(lineno)d] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )


# Вызываем настройку логирования при импорте модуля
setup_logging()

# Создаем логгер для этого модуля
logger = logging.getLogger("request")


@pytest.fixture()
def new_fixture():
    pass


@pytest.fixture(scope="function")
def selenium():
    """Фикстура для создания драйвера браузера"""
    # Логирование до запуска браузера
    logger.info("Starting browser initialization...")

    print("\n🚀 Запуск браузера Chrome...")

    # Настройка опций Chrome
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")

    # Создаем драйвер
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    # Логирование после запуска браузера
    logger.info(f"Browser started successfully. Session ID: {driver.session_id}")

    yield driver

    # Логирование перед закрытием браузера
    logger.info("Closing browser...")
    print("🔚 Закрытие браузера...")
    driver.quit()
    logger.info("Browser closed successfully")
