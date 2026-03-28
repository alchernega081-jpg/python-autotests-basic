import pytest
import allure
import re
from playwright.sync_api import Page, expect, sync_playwright


@pytest.fixture
def set_up_browser():
    """Фикстура для настройки и закрытия браузера"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@allure.feature('GitHub Advanced Search')
@allure.story('Search Repositories')
class TestGitHubAdvancedSearch:
    @allure.title('Поиск репозиториев с количеством звёзд >20000 на Python с файлом environment.yml')
    def test_search_repositories_with_stars(self, set_up_browser):
        page = set_up_browser

        # Шаг 1: Открыть страницу расширенного поиска
        print("\n1. Открываем страницу расширенного поиска...")
        with allure.step('Открытие страницы расширенного поиска'):
            page.goto("https://github.com/search/advanced")
            page.wait_for_load_state("networkidle")
            print("   ✓ Страница расширенного поиска открыта")

        # Шаг 2: В поле языка выбрать Python
        print("2. Выбираем язык Python...")
        with allure.step('Выбор языка Python из выпадающего списка'):
            language_dropdown = page.locator("#search_language")
            expect(language_dropdown).to_be_visible()
            language_dropdown.select_option(label="Python")
            print("   ✓ Выбран язык: Python")
            page.wait_for_timeout(1000)

        # Шаг 3: В поле количества звёзд выбрать >20000
        print("3. Указываем количество звёзд >20000...")
        with allure.step('Ввод количества звёзд >20000'):
            stars_input = page.locator("#search_stars")
            expect(stars_input).to_be_visible()
            stars_input.fill(">20000")

            entered_value = stars_input.input_value()
            print(f"   ✓ Указано количество звёзд: >20000 (введено: {entered_value})")
            assert "20000" in entered_value, "Значение не введено корректно"
            page.wait_for_timeout(1000)

        # Шаг 4: В поле с названием файла выбрать environment.yml
        print("4. Указываем имя файла environment.yml...")
        with allure.step('Ввод имени файла environment.yml'):
            filename_input = page.locator("#search_filename")
            expect(filename_input).to_be_visible()
            filename_input.fill("environment.yml")

            entered_filename = filename_input.input_value()
            print(f"   ✓ Указано имя файла: environment.yml (введено: {entered_filename})")
            assert "environment.yml" in entered_filename, "Имя файла не введено корректно"
            page.wait_for_timeout(1000)

        # Шаг 5: Нажать на кнопку поиска
        print("5. Нажимаем кнопку поиска...")
        with allure.step('Нажатие кнопки поиска'):
            # Вариант 1: Используем ID формы или более точный локатор
            # Кнопка поиска находится в форме advanced_search
            search_button = page.locator("#adv_code_search button[type='submit']")

            # Альтернативные варианты:
            # search_button = page.locator("form#adv_code_search button[type='submit']")
            # search_button = page.locator("button[type='submit']").first
            # search_button = page.get_by_role("button", name="Search").first

            expect(search_button).to_be_visible()
            search_button.click()
            print("   ✓ Кнопка поиска нажата, выполняется переход к результатам")

            # Ждем загрузку результатов
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)

        # Шаг 6: Проверить звёзды >20000
        print("6. Проверяем количество звёзд в результатах поиска...")
        with allure.step('Проверка количества звёзд в найденных репозиториях'):
            # Ждем появления результатов
            page.wait_for_selector("div[role='main']", timeout=15000)

            # Находим все репозитории в результатах
            repos = page.locator("div[class*='Box-row']")
            repos_count = repos.count()

            print(f"   ✓ Найдено репозиториев: {repos_count}")
            allure.attach(
                f"Найдено репозиториев: {repos_count}",
                name="Количество результатов",
                attachment_type=allure.attachment_type.TEXT
            )

            assert repos_count > 0, "Результаты поиска не найдены"

            # Проверяем первый репозиторий
            first_repo = repos.first

            # Ищем элемент с количеством звёзд
            stars_element = first_repo.locator("a[href$='stargazers']")
            if stars_element.count() == 0:
                stars_element = first_repo.locator("a[href*='stargazers']")
            if stars_element.count() == 0:
                stars_element = first_repo.locator("span[aria-label*='stars']")

            assert stars_element.count() > 0, "Не удалось найти элемент с количеством звёзд"

            stars_text = stars_element.first.text_content().strip()
            print(f"   Текст с звёздами: '{stars_text}'")

            # Извлекаем число из текста
            stars_count = self._extract_stars_count(stars_text)

            print(f"   ✓ Количество звёзд: {stars_count}")

            # Проверяем, что количество звёзд больше 20000
            assert stars_count > 20000, f"Количество звёзд: {stars_count} (должно быть >20000)"

            print(f"\n✅ ТЕСТ ПРОЙДЕН! Первый репозиторий имеет {stars_count} звёзд >20000")
            allure.attach(
                f"Первый репозиторий имеет {stars_count} звёзд, что > 20000",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT
            )

    def _extract_stars_count(self, stars_text: str) -> int:
        """Извлекает количество звёзд из текста"""
        stars_text = stars_text.lower().strip()
        stars_text = re.sub(r'stars?', '', stars_text).strip()

        # Обработка формата с k (тысячи)
        match = re.match(r'^([\d.]+)k$', stars_text)
        if match:
            number = float(match.group(1))
            return int(number * 1000)

        # Обработка формата с запятыми
        stars_text = stars_text.replace(',', '')

        # Извлечение числа
        numbers = re.findall(r'\d+', stars_text)
        if numbers:
            return int(numbers[0])

        return 0