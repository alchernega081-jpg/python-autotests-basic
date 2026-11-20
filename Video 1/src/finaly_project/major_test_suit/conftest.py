import os
import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Создаем папку для логов, если её нет
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, 'test.log')

# Настройка логирования программно
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s][%(asctime)s][%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),  # Вывод в консоль
        logging.FileHandler(log_file_path, 'a', 'utf-8')  # Вывод в файл
    ]
)

# Устанавливаем уровень для консоли (INFO и выше)
console = logging.getLogger().handlers[0]
console.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.info("Логирование настроено")
logger.info(f"Логи будут сохранены в: {log_file_path}")


#@pytest.fixture(scope="function")
#def set_up_browser():
    #"""Фикстура для инициализации и закрытия браузера"""
    #logger = logging.getLogger(__name__)

    #logger.info("=" * 50)
    #logger.info("Инициализация нового теста")

    #driver = webdriver.Chrome()
    #driver.maximize_window()
    #logger.debug("Драйвер Chrome инициализирован, окно развернуто")

    #yield driver

    #logger.info("Закрытие драйвера Chrome")
    #driver.quit()
    #logger.info("Тест завершен")
    #logger.info("=" * 50)
    #driver.quit()
    #logger.info("Тест завершен")
    #logger.info("=" * 50)

@pytest.fixture(scope="function")
def set_up_browser():
    """Фикстура для инициализации и закрытия браузера"""
    logger = logging.getLogger(__name__)

    logger.info("=" * 50)
    logger.info("Инициализация нового теста")

    # ✅ Настройка headless-режима для GitHub Actions
    options = Options()
    options.add_argument("--headless=new")       # без окна браузера
    options.add_argument("--no-sandbox")         # для Linux-окружения GitHub
    options.add_argument("--disable-dev-shm-usage")  # предотвращает падение Chrome
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    logger.debug("Драйвер Chrome инициализирован, окно развернуто")

    yield driver

    logger.info("Закрытие драйвера Chrome")
    driver.quit()
    logger.info("Тест завершен")
    logger.info("=" * 50)