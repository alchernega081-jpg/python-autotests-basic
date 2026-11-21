import pytest
import allure
from playwright.sync_api import Page, expect, sync_playwright


@pytest.fixture
def set_up_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=True для безголового режима
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        with allure.step('Открытие главной страницы GitHub'):
            page.goto('https://github.com')
        yield page
        context.close()
        browser.close()


@allure.feature('Full Accounts')
@allure.story('Waiting page load')
class TestGitHubIssues:
    @allure.title('Проверка поиска задач с "bug" в заголовке')
    def test_search_issues_with_bug_in_title(self, set_up_browser):
        page = set_up_browser

        print("\n1. Открываем страницу Issues репозитория...")
        with allure.step('Открытие страницы Issues'):
            page.goto("https://github.com/microsoft/vscode/issues")
            page.wait_for_load_state("networkidle")

        print("2. Находим поле поиска...")
        with allure.step('Поиск поля ввода поиска'):
            search_input = page.locator("input[placeholder='Search Issues']")
            expect(search_input).to_be_visible()
            print("   ✓ Поле поиска найдено")

        print("3. Кликаем по полю...")
        with allure.step('Клик по полю поиска'):
            search_input.click()
            print("   ✓ Клик выполнен")

        print("4. Очищаем поле...")
        with allure.step('Очистка поля поиска'):
            search_input.fill("")
            print("   ✓ Поле очищено")

        print("5. Вводим фильтр 'in:title bug'...")
        with allure.step('Ввод поискового запроса'):
            search_input.fill("in:title bug")
            print("   ✓ Текст введен")

        # Проверяем введенный текст
        entered_text = search_input.input_value()
        print(f"   Введено: '{entered_text}'")

        print("6. Нажимаем Enter...")
        with allure.step('Нажатие Enter для выполнения поиска'):
            search_input.press("Enter")
            page.wait_for_load_state("networkidle")
            print("   ✓ Поиск выполнен")

        print("7. Получаем список задач...")
        with allure.step('Получение заголовков задач'):
            # Ожидаем загрузки результатов
            page.wait_for_selector("a[data-hovercard-type='issue'], .js-issue-title", timeout=15000)

            # Получаем заголовки задач
            titles = page.locator("a[data-hovercard-type='issue']").all()
            if not titles:
                titles = page.locator(".js-issue-title").all()

            # Фильтруем непустые заголовки
            issue_titles = []
            for title in titles:
                text = title.text_content()
                if text and text.strip():
                    issue_titles.append(text.strip())

            if issue_titles:
                print(f"   ✓ Найдено задач: {len(issue_titles)}")

                # Проверяем наличие слова bug
                issues_without_bug = []
                for title_text in issue_titles:
                    if "bug" not in title_text.lower():
                        issues_without_bug.append(title_text)

                if len(issues_without_bug) == 0:
                    print(f"\n✅ ТЕСТ ПРОЙДЕН! Все {len(issue_titles)} задач содержат слово 'bug'")
                else:
                    print(f"\n❌ ТЕСТ НЕ ПРОЙДЕН! Найдено {len(issues_without_bug)} задач без слова 'bug'")
                    for title in issues_without_bug[:5]:  # Показываем первые 5 проблемных задач
                        print(f"   - {title}")

                assert len(issues_without_bug) == 0, f"Найдено задач без 'bug': {len(issues_without_bug)}"
            else:
                print("   ⚠ Задачи не найдены")
                assert False, "Задачи не найдены после поиска"