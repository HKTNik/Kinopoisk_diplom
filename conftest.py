from typing import Generator, Dict
import pytest
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from config import Config


@pytest.fixture(scope="session")
def api_headers() -> Dict[str, str]:
    return {
        "X-API-KEY": Config.API_KEY,
        "Accept": "application/json"
    }


@pytest.fixture(scope="function")
def page() -> Generator[Page, None, None]:
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False)
        context: BrowserContext = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )
        new_page: Page = context.new_page()
        new_page.set_default_timeout(Config.TIMEOUT)
        yield new_page
        context.close()
        browser.close()
