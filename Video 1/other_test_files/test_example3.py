from selenium.webdriver import  Remote
from selenium.webdriver.chrome.options import Options as ChromeOptions
import pytest

from yandex_script import driver


@pytest.fixture()
def set_up_browser():
    driver = Remote(
        command_executor="http://127.0.0.1:4444/wd/hub",
        options=options  # Используем параметр options вместо desired_capabilities
    options = ChromeOptions()
    options.set_capability("browserName", "chrome")
    options.set_capability("browserVersion", "latest")
    yield driver
    driver.quit()


class TestExample:#Test Suite
    def test_example(self, set_up_browser):#Test Case
        driver = set_up_browser
        options = ChromeOptions()
        options.set_capability("browserName", "chrome")
        options.set_capability("browserVersion", "latest")

        driver = Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            options=options  # Используем параметр options вместо desired_capabilities
        )
        driver.get("https://skillbox.ru")
        assert 'Skillbox - образовательная платформа с онлайн-курсами.' == driver.title
        #print("Страница загружена успешно!")

        # Закрытие через close() и quit()
        driver.close()
        driver.quit()

if __name__ == "__main__":
    test = TestExample()
    test.test_example()

