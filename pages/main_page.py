import allure
from playwright.sync_api import Page, Locator, expect
from config import Config


class KinopoiskMainPage:
    def __init__(self, page: Page) -> None:
        self.page: Page = page
        # Универсальный локатор строки поиска в шапке Кинопоиска
        self.search_input: Locator = page.locator("input[placeholder*='Фильмы, сериалы, персоны'], input[name='kp_query']").first

    @allure.step("Открыть главную страницу Кинопоиска")
    def open(self) -> None:
        self.page.goto(Config.UI_BASE_URL, wait_until="domcontentloaded")

    @allure.step("Выполнить поиск по запросу: '{query}'")
    def search_for(self, query: str) -> None:
        if self.search_input.is_visible(timeout=3000):
            self.search_input.fill(query)
            self.search_input.press("Enter")
        else:
            # Резервный переход на страницу поиска, если шапка скрыта адаптивным меню
            self.page.goto(f"{Config.UI_BASE_URL}/index.php?kp_query={query}", wait_until="domcontentloaded")

    @allure.step("Проверить загрузку основного контента главной страницы")
    def check_main_content_loaded(self) -> None:
        expect(self.page.locator("body")).to_be_visible()
