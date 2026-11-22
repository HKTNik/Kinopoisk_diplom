import re
import allure
from playwright.sync_api import Page, expect
from pages.main_page import KinopoiskMainPage
from config import Config


@allure.feature("UI Тестирование Кинопоиск")
class TestKinopoiskUI:

    @allure.title("UI-1: Проверка загрузки главной страницы и заголовка")
    def test_main_page_elements(self, page: Page) -> None:
        main_page = KinopoiskMainPage(page)
        main_page.open()

        with allure.step("Проверить заголовок страницы и отображение тела документа"):
            expect(page).to_have_title(re.compile("Кинопоиск"))
            main_page.check_main_content_loaded()

    @allure.title("UI-2: Поиск фильма по названию")
    def test_search_movie_ui(self, page: Page) -> None:
        main_page = KinopoiskMainPage(page)
        main_page.open()
        main_page.search_for("Интерстеллар")

        with allure.step("Проверить, что открылась страница выдачи с найденным фильмом"):
            expect(page.locator("text=Интерстеллар").first).to_be_visible()

    @allure.title("UI-3: Открытие детальной карточки фильма по прямой ссылке")
    def test_open_movie_card_details(self, page: Page) -> None:
        with allure.step("Перейти в карточку фильма 'Начало' (/film/447301/)"):
            page.goto(f"{Config.UI_BASE_URL}/film/447301/", wait_until="domcontentloaded")

        with allure.step("Проверить наличие заголовка и информации о фильме"):
            expect(page.locator("h1").first).to_contain_text("Начало")

    @allure.title("UI-4: Поиск персоны (актера)")
    def test_search_actor_ui(self, page: Page) -> None:
        main_page = KinopoiskMainPage(page)
        main_page.open()
        main_page.search_for("Леонардо ДиКаприо")

        with allure.step("Проверить наличие карточки актера в выдаче"):
            expect(page.locator("text=Леонардо ДиКаприо").first).to_be_visible()

    @allure.title("UI-5: Открытие каталога фильмов жанра 'Комедия'")
    def test_genre_catalog_navigation(self, page: Page) -> None:
        with allure.step("Перейти в список фильмов жанра 'Комедия'"):
            page.goto(f"{Config.UI_BASE_URL}/lists/movies/genre--comedy/", wait_until="domcontentloaded")

        with allure.step("Проверить заголовок списка категорий"):
            expect(page.locator("h1").first).to_contain_text("Комедии")
