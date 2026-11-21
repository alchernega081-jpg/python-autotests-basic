from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options as ChromeOptions
import pytest


@pytest.fixture()
def set_up_browser():
    print("\n=== Запуск фикстуры ===")
    options = ChromeOptions()
    options.set_capability("browserName", "chrome")
    options.set_capability("browserVersion", "latest")

    driver = Remote(
        command_executor="http://127.0.0.1:4444/wd/hub",
        options=options
    )

    yield driver
    print("\n=== Закрытие драйвера ===")
    driver.quit()


import allure

@allure.step('Проверка заголовка страницы')
def check_title(driver, title):
    assert title == driver.title




class TestExample: #Test Suite
    def test_example(self, set_up_browser):
        print("\n=== Выполняется test_example 1 ===")
        driver = set_up_browser
        driver.get("https://skillbox.ru")
        check_title( driver=driver, title='Skillbox – образовательная платформа с онлай-курсами.')

    def test_example_2(self, set_up_browser): # Test Case
        print("\n=== Выполняется test_example 2 ===")
        driver = set_up_browser
        driver.get("https://skillbox.ru")
        check_title(driver=driver, title='Skillbox ')

    def test_example_3(self, set_up_browser): # Test Case
        print("\n=== Выполняется test_example 3 ===")
        driver = set_up_browser
        driver.get("https://skillbox.ru")
        assert 'Skillbox ' == driver.title

    def test_example_4(self, set_up_browser): # Test Case
        print("\n=== Выполняется test_example 4 ===")
        driver = set_up_browser
        driver.get("https://skillbox.ru")
        assert 'Skillbox ' == driver.title


# Для отладки лучше не использовать pytest.main()
# Просто запускайте файл через pytest в командной строке

#if __name__ == "__main__":
    # Временно закомментируйте для теста
    # pytest.main([__file__, "-v", "-s"])  # -s для вывода print
    #print("Запустите тест командой: pytest test_file.py -v -s")