import pytest
import allure
import time
from playwright.sync_api import Page, expect, sync_playwright


@pytest.fixture
def set_up_browser():
    """Фикстура для настройки и закрытия браузера"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=True для CI/CD
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@allure.feature('GitHub Commit Graph')
@allure.story('Commit Activity')
class TestGitHubCommitGraph:
    @allure.title('Проверка тултипа на графике коммитов')
    def test_commit_graph_tooltip(self, set_up_browser):
        page = set_up_browser

        # Шаг 1: Открыть страницу
        print("\n1. Открываем страницу графика коммитов...")
        with allure.step('Открытие страницы графика коммитов'):
            page.goto("https://github.com/microsoft/vscode/graphs/commit-activity")
            page.wait_for_load_state("networkidle")
            print("   ✓ Страница открыта")

        # Шаг 2: Ожидаем загрузку графика и находим столбцы
        print("\n2. Ожидаем загрузку графика...")
        with allure.step('Ожидание загрузки графика'):
            # Ждем загрузки SVG элемента графика
            page.wait_for_selector("svg.highcharts-root", timeout=15000)
            page.wait_for_timeout(2000)  # Дополнительное ожидание для полной загрузки данных
            print("   ✓ График загружен")

        print("\n3. Находим все столбцы графика...")
        with allure.step('Поиск столбцов графика'):
            # Пробуем различные селекторы для столбцов
            bars = page.locator("rect.highcharts-point, .highcharts-point, [class*='highcharts-point']")

            # Если не нашли, пробуем другие селекторы
            if bars.count() == 0:
                bars = page.locator("rect[class*='point']")
            if bars.count() == 0:
                bars = page.locator("g.highcharts-series rect")

            bars_count = bars.count()
            print(f"   ✓ Найдено столбцов: {bars_count}")
            allure.attach(
                f"Найдено столбцов на графике: {bars_count}",
                name="Количество столбцов",
                attachment_type=allure.attachment_type.TEXT
            )

            assert bars_count > 0, "Не найдено столбцов на графике"

        # Шаг 4: Навести мышку на первый столбец
        print("\n4. Наводим мышку на первый столбец...")
        with allure.step('Наведение мыши на первый столбец'):
            first_bar = bars.first

            # Прокручиваем к элементу, если необходимо
            first_bar.scroll_into_view_if_needed()
            page.wait_for_timeout(500)

            # Наводим мышку
            first_bar.hover()
            print("   ✓ Наведение выполнено")
            page.wait_for_timeout(2000)  # Ждем появления тултипа

        # Шаг 5: Проверяем, что тултип появился
        print("\n5. Проверяем появление тултипа...")
        with allure.step('Проверка отображения тултипа'):
            # Ждем появления тултипа
            tooltip = page.locator("div.highcharts-tooltip")

            try:
                # Ожидаем, что тултип станет видимым
                expect(tooltip).to_be_visible(timeout=5000)

                # Получаем текст тултипа для дополнительной проверки
                tooltip_text = tooltip.text_content()
                print(f"   ✓ Тултип отображается")
                print(f"   📊 Текст тултипа: {tooltip_text[:100] if tooltip_text else 'Не найден'}")

                # Сохраняем текст тултипа в отчет
                allure.attach(
                    tooltip_text,
                    name="Текст тултипа",
                    attachment_type=allure.attachment_type.TEXT
                )

                print("   ✅ Тултип успешно отобразился")

            except Exception as e:
                print(f"   ❌ Тултип не появился: {str(e)}")
                # Делаем скриншот для отладки
                screenshot = page.screenshot()
                allure.attach(
                    screenshot,
                    name="Скриншот при ошибке",
                    attachment_type=allure.attachment_type.PNG
                )
                raise AssertionError("Тултип не появился после наведения мыши")

        print("\n✅ ТЕСТ ПРОЙДЕН! Тултип успешно отобразился при наведении на столбец графика")
        allure.attach(
            "Тултип успешно отобразился при наведении на столбец графика",
            name="Результат теста",
            attachment_type=allure.attachment_type.TEXT
        )