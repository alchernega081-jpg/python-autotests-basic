import os
import logging
import logging.config
import pytest
from os import path

from other_test_files.conftest import pytest_plugins

pytest_plugins = [
    "src.fixtures",
    "src.actions.base",
    "src.actions.wait"
]

# Закомментировали fileConfig
lof_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.ini')
logging.config.fileConfig(lof_file_path)

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s][%(levelname)s][%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),  # вывод в консоль
        logging.FileHandler('log.txt', 'w')  # запись в файл (убрал ../..)
    ]
)

def pytest_addoption(parser):
    parser.addini("selenium_url", "Selenium Hub url")
    parser.addini("browser_name", "Browser name for tests")
    parser.addini("browser_version", "Browser version for tests")
    parser.addini("headless", "Run browser in headless mode", default="False")