from typing import Dict, Any
import allure
import pytest
import requests
from config import Config


@allure.feature("API Тестирование ПоискКино")
class TestPoiskKinoAPI:

    @allure.title("API-1 (Позитивный): Поиск фильма по названию")
    @pytest.mark.parametrize("movie_name", ["Аватар", "Интерстеллар"])
    def test_search_movie_by_name(self, api_headers: Dict[str, str], movie_name: str) -> None:
        url: str = f"{Config.API_BASE_URL}/movie/search"
        params: Dict[str, str] = {"query": movie_name}

        with allure.step(f"Отправка GET-запроса на поиск фильма '{movie_name}'"):
            response: requests.Response = requests.get(url, headers=api_headers, params=params)

        with allure.step("Проверка статус-кода 200 и структуры ответа"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
            data: Dict[str, Any] = response.json()
            assert "docs" in data and len(data["docs"]) > 0, "Список результатов пуст"
            assert "id" in data["docs"][0], "У найденного фильма отсутствует поле id"

    @allure.title("API-2 (Позитивный): Получение детальной карточки фильма по ID")
    def test_get_movie_by_id(self, api_headers: Dict[str, str]) -> None:
        movie_id: int = 258687  # ID фильма 'Интерстеллар'
        url: str = f"{Config.API_BASE_URL}/movie/{movie_id}"

        with allure.step(f"Запрос карточки фильма с ID {movie_id}"):
            response: requests.Response = requests.get(url, headers=api_headers)

        with allure.step("Проверка соответствия ID и наличия ключевых полей"):
            assert response.status_code == 200
            data: Dict[str, Any] = response.json()
            assert data.get("id") == movie_id
            assert data.get("name") == "Интерстеллар"

    @allure.title("API-3 (Позитивный): Получение случайного фильма с фильтром по жанру")
    def test_get_random_comedy_movie(self, api_headers: Dict[str, str]) -> None:
        url: str = f"{Config.API_BASE_URL}/movie/random"
        params: Dict[str, str] = {"genres.name": "комедия"}

        with allure.step("Отправка запроса на генерацию случайной комедии"):
            response: requests.Response = requests.get(url, headers=api_headers, params=params)

        with allure.step("Проверка статуса 200 и наличия жанра 'комедия' в ответе"):
            assert response.status_code == 200
            data: Dict[str, Any] = response.json()
            genres: list[str] = [g.get("name", "") for g in data.get("genres", [])]
            assert "комедия" in genres, f"Жанр комедия не найден в списке: {genres}"

    @allure.title("API-4 (Негативный): Запрос с невалидным токеном авторизации (401)")
    def test_unauthorized_request(self) -> None:
        url: str = f"{Config.API_BASE_URL}/movie/search"
        invalid_headers: Dict[str, str] = {"X-API-KEY": "invalid_token_12345_qa"}

        with allure.step("Отправка запроса с неверным X-API-KEY"):
            response: requests.Response = requests.get(url, headers=invalid_headers, params={"query": "Аватар"})

        with allure.step("Проверка получения ошибки 401 Unauthorized"):
            assert response.status_code == 401

    @allure.title("API-5 (Негативный): Запрос фильма по несуществующему ID (404)")
    def test_movie_not_found(self, api_headers: Dict[str, str]) -> None:
        non_existent_id: int = 9999999
        url: str = f"{Config.API_BASE_URL}/movie/{non_existent_id}"

        with allure.step(f"Запрос несуществующего фильма с ID {non_existent_id}"):
            response: requests.Response = requests.get(url, headers=api_headers)

        with allure.step("Проверка получения ошибки 404 Not Found"):
            assert response.status_code == 404
