import pytest
import allure
import re
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


@allure.feature('Skillbox Courses')
@allure.story('Filter Courses')
class TestSkillboxFilters:
    @allure.title('Проверка фильтрации курсов по профессии, длительности и тематике')
    def test_filter_courses_by_profession_duration_theme(self, set_up_browser):
        page = set_up_browser

        # Шаг 1: Открыть страницу
        print("\n1. Открываем страницу Skillbox...")
        with allure.step('Открытие страницы Skillbox'):
            page.goto("https://skillbox.ru/code/")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)
            print("   ✓ Страница открыта")

        # Шаг 2: Выбрать вкладку "Профессия"
        print("\n2. Выбираем вкладку 'Профессия'...")
        with allure.step('Выбор вкладки "Профессия"'):
            profession_tab = page.locator(
                "//button[contains(@class, 'programs-filter-desktop__tab')]//span[contains(@class, 'ui-tab__text') and contains(text(), 'Профессия')]"
            )
            expect(profession_tab).to_be_visible()
            profession_tab.click()
            print("   ✓ Вкладка 'Профессия' выбрана")
            page.wait_for_timeout(2000)

        # Шаг 3: Выбрать длительность от 6 до 12 месяцев
        print("\n3. Выбираем длительность от 6 до 12 месяцев...")
        with allure.step('Выбор длительности курса'):
            # Находим и открываем выпадающий список "Длительность"
            duration_button = page.locator(
                "//button[contains(@class, 'ui-round-select__field')]//span[contains(text(), 'Длительность')]/ancestor::button"
            )
            expect(duration_button).to_be_visible()
            duration_button.scroll_into_view_if_needed()
            page.wait_for_timeout(500)
            duration_button.click()
            print("   ✓ Выпадающий список 'Длительность' открыт")
            page.wait_for_timeout(1000)

            # Выбираем диапазон "От 6 до 12 мес."
            duration_option = page.locator(
                "//li[contains(@class, 'ui-round-select__item') and contains(text(), 'От 6 до 12 мес.')]"
            )
            expect(duration_option).to_be_visible()
            duration_option.scroll_into_view_if_needed()
            page.wait_for_timeout(500)
            duration_option.click()
            print("   ✓ Выбран диапазон 'От 6 до 12 мес.'")
            page.wait_for_timeout(2000)

        # Шаг 4: Выбрать тематику "Python"
        print("\n4. Выбираем тематику 'Python'...")
        with allure.step('Выбор тематики Python'):
            # Находим и открываем выпадающий список "Тематика"
            theme_button = page.locator(
                "//button[contains(@class, 'ui-round-select__field')]//span[contains(text(), 'Тематика')]/ancestor::button"
            )
            expect(theme_button).to_be_visible()
            theme_button.scroll_into_view_if_needed()
            page.wait_for_timeout(1000)
            theme_button.click()
            print("   ✓ Выпадающий список 'Тематика' открыт")
            page.wait_for_timeout(1000)

            # Находим поле поиска и вводим "Python"
            search_input = page.locator("div.ui-round-select-popup__header input[placeholder='Поиск']")
            expect(search_input).to_be_visible()
            search_input.fill("Python")
            print("   ✓ В поле поиска введено 'Python'")
            page.wait_for_timeout(2000)

            # Находим элемент "Python" в списке и кликаем по нему
            python_option = page.locator("//li[contains(@class, 'ui-round-select__item') and text()='Python']")
            expect(python_option).to_be_visible()
            python_option.scroll_into_view_if_needed()
            page.wait_for_timeout(500)
            python_option.click()
            print("   ✓ Выбран чекбокс 'Python'")
            page.wait_for_timeout(1000)

            # Нажимаем кнопку "Применить"
            apply_button = page.locator("div.ui-round-select-popup__footer button.ui-button")
            expect(apply_button).to_be_visible()
            apply_button.click()
            print("   ✓ Нажата кнопка 'Применить'")
            page.wait_for_timeout(3000)

            print("   ✓ Фильтр тематики применен")

        # Шаг 5: Получить все курсы на странице
        print("\n5. Получаем список курсов после фильтрации...")
        with allure.step('Получение списка курсов'):
            # Ждем загрузки карточек курсов
            page.wait_for_selector("div[class*='card'], div[class*='Card']", timeout=15000)
            page.wait_for_timeout(2000)

            # Находим все карточки курсов
            courses = page.locator("div[class*='card']")
            if courses.count() == 0:
                courses = page.locator("a[class*='course']")

            courses_count = courses.count()
            print(f"   ✓ Найдено курсов: {courses_count}")
            allure.attach(
                f"Найдено курсов после фильтрации: {courses_count}",
                name="Количество курсов",
                attachment_type=allure.attachment_type.TEXT
            )

            assert courses_count > 0, "Не найдено ни одного курса после фильтрации"

        # Шаг 6: Проверить, что курсы соответствуют выбранным фильтрам
        print("\n6. Проверяем соответствие курсов выбранным фильтрам...")
        print("   " + "=" * 65)

        with allure.step('Проверка соответствия курсов фильтрам'):
            invalid_courses = []
            course_details = []

            # Проверяем первые 10 курсов
            check_count = min(courses_count, 10)

            for i in range(check_count):
                course = courses.nth(i)
                print(f"\n   Курс {i + 1}:")

                # Получаем название курса
                title = self._get_course_title(course)
                print(f"      📚 Название: {title[:60]}")

                # Получаем длительность курса
                duration = self._get_course_duration(course)
                print(f"      ⏱ Длительность: {duration}")

                # Получаем тематику курса
                theme = self._get_course_theme(course)
                print(f"      🏷 Тематика: {theme}")

                # Проверяем соответствие фильтрам
                checks = {
                    'длительность': self._check_duration(duration, 6, 12),
                    'тематика': self._check_theme(theme, "Python")
                }

                # Выводим результаты проверок
                status = "✅"
                for check_name, passed in checks.items():
                    if not passed:
                        status = "❌"
                        invalid_courses.append({
                            'index': i + 1,
                            'title': title,
                            'duration': duration,
                            'theme': theme,
                            'failed_checks': [k for k, v in checks.items() if not v]
                        })
                        print(f"      ❌ Не пройдена проверка: {check_name}")

                print(f"      {status} Статус: {'Пройден' if all(checks.values()) else 'Не пройден'}")

                course_details.append({
                    'index': i + 1,
                    'title': title,
                    'duration': duration,
                    'theme': theme,
                    'passed': all(checks.values())
                })

            # Формируем отчет
            print("\n" + "=" * 65)
            print("\n📊 ИТОГИ ПРОВЕРКИ:")
            print(f"   Всего проверено курсов: {check_count}")
            print(f"   ✅ Прошли проверку: {len([c for c in course_details if c['passed']])}")
            print(f"   ❌ Не прошли проверку: {len(invalid_courses)}")

            if invalid_courses:
                print("\n❌ КУРСЫ, НЕ СООТВЕТСТВУЮЩИЕ ФИЛЬТРАМ:")
                for course in invalid_courses[:5]:
                    print(f"   {course['index']}. {course['title'][:50]}...")
                    print(f"      Длительность: {course['duration']}")
                    print(f"      Тематика: {course['theme']}")
                    print(f"      Не пройдены: {', '.join(course['failed_checks'])}")

            # Сохраняем детали в Allure
            allure.attach(
                self._format_course_report(course_details),
                name="Детальная проверка курсов",
                attachment_type=allure.attachment_type.TEXT
            )

            # Основная проверка
            assert len(invalid_courses) == 0, f"Найдено {len(invalid_courses)} курсов, не соответствующих фильтрам"

            print(f"\n✅ ТЕСТ ПРОЙДЕН! Все {check_count} проверенных курсов соответствуют выбранным фильтрам")

    def _get_course_title(self, course) -> str:
        """Получает название курса"""
        try:
            title_element = course.locator("h3, [class*='title']").first
            if title_element.is_visible():
                return title_element.text_content().strip()
        except:
            pass
        return "Не найден"

    def _get_course_duration(self, course) -> str:
        """Получает длительность курса"""
        try:
            # Пробуем найти элемент с длительностью
            duration_selectors = [
                "[class*='duration']",
                "[class*='time']",
                "span:has-text('мес')",
                "span:has-text('месяц')"
            ]

            for selector in duration_selectors:
                duration_element = course.locator(selector).first
                if duration_element.is_visible():
                    text = duration_element.text_content().strip()
                    if text and any(x in text.lower() for x in ['мес', 'месяц']):
                        return text
        except:
            pass
        return "Не указана"

    def _get_course_theme(self, course) -> str:
        """Получает тематику курса"""
        try:
            # Пробуем найти элемент с тематикой
            theme_selectors = [
                "[class*='theme']",
                "[class*='tag']",
                "[class*='label']",
                "span:has-text('Python')",
                "span:has-text('Java')"
            ]

            for selector in theme_selectors:
                theme_element = course.locator(selector).first
                if theme_element.is_visible():
                    text = theme_element.text_content().strip()
                    if text:
                        return text
        except:
            pass
        return "Не указана"

    def _check_duration(self, duration_text: str, min_months: int, max_months: int) -> bool:
        """Проверяет, что длительность курса входит в указанный диапазон"""
        if not duration_text or duration_text == "Не указана":
            return False

        # Извлекаем число месяцев из текста
        months = self._extract_months(duration_text)
        if months is None:
            return False

        return min_months <= months <= max_months

    def _extract_months(self, duration_text: str) -> int:
        """Извлекает количество месяцев из текста"""
        # Ищем числа в тексте
        numbers = re.findall(r'\d+', duration_text)
        if not numbers:
            return None

        # Проверяем, есть ли указание на месяцы
        if 'мес' in duration_text.lower() or 'месяц' in duration_text.lower():
            return int(numbers[0])

        # Если есть диапазон типа "6-12 мес", берем среднее
        if '-' in duration_text:
            nums = [int(n) for n in numbers]
            if len(nums) >= 2:
                return (nums[0] + nums[1]) // 2

        return int(numbers[0]) if numbers else None

    def _check_theme(self, theme_text: str, expected_theme: str) -> bool:
        """Проверяет, что тематика курса соответствует ожидаемой"""
        if not theme_text or theme_text == "Не указана":
            return False

        return expected_theme.lower() in theme_text.lower()

    def _format_course_report(self, course_details: list) -> str:
        """Форматирует отчет о проверке курсов"""
        report = "Результаты проверки курсов:\n\n"
        report += "=" * 80 + "\n"

        for course in course_details:
            status = "✅ ПРОЙДЕН" if course['passed'] else "❌ НЕ ПРОЙДЕН"
            report += f"\nКурс #{course['index']}: {status}\n"
            report += f"  Название: {course['title']}\n"
            report += f"  Длительность: {course['duration']}\n"
            report += f"  Тематика: {course['theme']}\n"
            report += "-" * 40 + "\n"

        return report
