import pytest
import allure
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


@allure.feature('GitHub Issues')
@allure.story('Filter Issues by Author')
class TestGitHubIssues:
    @allure.title('Фильтрация задач по автору bpasero')
    def test_filter_issues_by_author_bpasero(self, set_up_browser):
        page = set_up_browser

        with allure.step('Открытие страницы Issues репозитория microsoft/vscode'):
            page.goto("https://github.com/microsoft/vscode/issues")
            page.wait_for_load_state("networkidle")

        with allure.step('Открытие меню фильтрации по автору'):
            # Нажимаем кнопку Author
            author_button = page.get_by_label("Filter by author")
            expect(author_button).to_be_visible()
            author_button.click()

        with allure.step('Поиск и выбор автора bpasero'):
            # Используем get_by_placeholder для более чистого кода
            author_search = page.get_by_placeholder("Filter authors")
            expect(author_search).to_be_visible()

            # Вводим имя автора
            author_search.fill("bpasero")

            # Ждем появления и кликаем по элементу автора
            author_option = page.get_by_text("bpasero", exact=True).first
            expect(author_option).to_be_visible()
            author_option.click()

            # Ждем применения фильтра и загрузки результатов
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)

        with allure.step('Проверка результатов фильтрации'):
            # Находим все задачи
            issues = page.locator("[data-testid='issue']")

            # Если не нашли, пробуем альтернативные селекторы
            if issues.count() == 0:
                issues = page.locator("[class*='issue']").filter(has=page.locator("a[data-hovercard-type='issue']"))

            issues_count = issues.count()
            assert issues_count > 0, "Задачи не найдены после применения фильтра"

            # Проверяем автора каждой задачи
            wrong_authors = []
            for i in range(issues_count):
                issue = issues.nth(i)

                # Ищем имя автора в задаче
                author_name = issue.locator("a[data-hovercard-type='user']").first

                if author_name.is_visible():
                    author_text = author_name.text_content().strip()
                    if author_text != "bpasero":
                        wrong_authors.append(author_text)

            # Формируем информативное сообщение об ошибке
            if wrong_authors:
                error_msg = f"Найдено {len(wrong_authors)} задач с другим автором: {', '.join(wrong_authors[:5])}"
                if len(wrong_authors) > 5:
                    error_msg += f" и еще {len(wrong_authors) - 5}"
                allure.attach(
                    f"Найдено задач: {issues_count}\n"
                    f"Задачи с неправильным автором: {len(wrong_authors)}\n"
                    f"Авторы: {', '.join(wrong_authors)}",
                    name="Результаты проверки",
                    attachment_type=allure.attachment_type.TEXT
                )
                assert False, error_msg
            else:
                allure.attach(
                    f"Все {issues_count} задач принадлежат автору bpasero",
                    name="Успешная проверка",
                    attachment_type=allure.attachment_type.TEXT
                )
                print(f"\n✅ Успешно! Все {issues_count} задач принадлежат автору bpasero")