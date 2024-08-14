import os

from dotenv import load_dotenv
import pytest
from playwright.sync_api import Playwright, Page

BROWSER = os.getenv('BROWSER') if os.getenv('BROWSER') is not None else 'chrome'
IS_HEADLESS = os.getenv('IS_HEADLESS') if os.getenv('IS_HEADLESS') is not None else False


@pytest.fixture(scope="session", autouse=True)
def envs():
    load_dotenv()


@pytest.fixture(scope="session")
def app_url():
    return os.getenv("APP_URL")


@pytest.fixture(scope="session")
def auth_url():
    return os.getenv("AUTH_URL")


@pytest.fixture(scope="session")
def page(playwright: Playwright):
    match BROWSER:
        case 'firefox':
            browser = playwright.firefox.launch(headless=IS_HEADLESS)
        case 'chrome':
            browser = playwright.chromium.launch(headless=IS_HEADLESS)
        case _:
            browser = playwright.chromium.launch(headless=IS_HEADLESS)
    page: Page = browser.new_page()
    yield page
    browser.close()
