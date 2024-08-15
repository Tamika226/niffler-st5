import os

from dotenv import load_dotenv
import pytest
from playwright.sync_api import Playwright, Page, expect, Browser

from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.identification_page import IdentificationPage
from pages.register_page import RegisterPage
from pages.profile_page import ProfilePage

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
def browser(playwright: Playwright):
    match BROWSER:
        case 'firefox':
            browser = playwright.firefox.launch(headless=IS_HEADLESS)
        case 'chrome':
            browser = playwright.chromium.launch(headless=IS_HEADLESS)
        case _:
            browser = playwright.chromium.launch(headless=IS_HEADLESS)
    yield browser
    browser.close()


@pytest.fixture
def page(browser: Browser) -> Page:
    page = browser.new_page()
    page.set_default_timeout(os.getenv("DEFAULT_TIMEOUT"))
    yield page
    page.close()


@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)


@pytest.fixture
def identification_page(page: Page):
    return IdentificationPage(page)


@pytest.fixture
def main_page(page: Page):
    return MainPage(page)


@pytest.fixture
def register_page(page: Page):
    return RegisterPage(page)


@pytest.fixture
def profile_page(page: Page):
    return ProfilePage(page)


@pytest.fixture
def login(page: Page, identification_page: IdentificationPage, login_page: LoginPage, main_page: MainPage, app_url):
    page.goto(app_url)
    identification_page.to_login()

    login_page.enter_username(os.getenv("DEFAULT_USER_LOGIN"))
    login_page.enter_password(os.getenv("DEFAULT_USER_PASSWORD"))
    login_page.click_button()

    expect(main_page.profile).to_be_visible()
