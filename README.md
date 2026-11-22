# Дипломный проект по автоматизации тестирования (UI + API)

Проект содержит набор независимых автотестов для проверки REST API сервиса **ПоискКино** (`api.poiskkino.dev`) и веб-интерфейса **Кинопоиск** (`kinopoisk.ru`).

## Стек технологий
* **Язык:** Python 3.10+
* **Фреймворк тестирования:** Pytest
* **API-тестирование:** Requests
* **UI-тестирование:** Playwright (паттерн Page Object)
* **Отчетность:** Allure Report

## Установка и запуск

1. Клонируйте репозиторий и перейдите в папку проекта:
   ```bash
   git clone <ссылка-на-ваш-репозиторий>
   cd kinopoisk_diploma_autotests
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv .venv
   # Для Windows:
   .venv\Scripts\activate
   # Для macOS/Linux:
   source .venv/bin/activate
   ```

3. Установите зависимости и браузер для Playwright:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

4. Укажите ваш API-ключ в файле `config.py` в поле `API_KEY`.

5. Запустите все тесты с сохранением результатов для Allure:
   ```bash
   pytest --alluredir=allure-results
   ```

6. Сгенерируйте и откройте отчет Allure (требуется установленный Allure CLI):
   ```bash
   allure serve allure-results
   ```
