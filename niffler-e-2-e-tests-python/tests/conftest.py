import os

from dotenv import load_dotenv
import pytest
from playwright.sync_api import Playwright, Page, expect, Browser

from helpers.app import App
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.identification_page import IdentificationPage
from pages.register_page import RegisterPage
from pages.profile_page import ProfilePage
from helpers.data_generator import TestDataGenerator


from clients.spends_client import SpendsHttpClient
from clients.categories_client import CategoriesHttpClient

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
def gateway_url():
    return os.getenv("GATEWAY_URL")


@pytest.fixture()
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
    new_page = browser.new_page()
    yield new_page
    new_page.close()


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


@pytest.fixture()
def app(page, login_page, identification_page, main_page, register_page,profile_page):
    return App(page, login_page, identification_page, main_page, register_page, profile_page)


@pytest.fixture
def login(page: Page, identification_page: IdentificationPage, login_page: LoginPage, main_page: MainPage, app_url):
    page.goto(app_url)
    identification_page.open_login()

    login_page.enter_username(os.getenv("DEFAULT_USER_LOGIN"))
    login_page.enter_password(os.getenv("DEFAULT_USER_PASSWORD"))
    login_page.click_submit()
    expect(main_page.profile).to_be_visible()

    token = page.evaluate("()=>window.sessionStorage.getItem('id_token')")
    return token


@pytest.fixture(scope="session")
def generator():
    generator = TestDataGenerator()
    return generator


@pytest.fixture()
def spends_client(gateway_url, login) -> SpendsHttpClient:
    return SpendsHttpClient(gateway_url, login)


@pytest.fixture()
def categories_client(gateway_url, login) -> CategoriesHttpClient:
    return CategoriesHttpClient(gateway_url, login)


@pytest.fixture()
def get_any_category(categories_client, generator):
    categories = categories_client.get_categories()
    if not categories:
        new_name = generator.word()
        categories_client.add_category(new_name)
        return new_name
    return categories[0]["category"]
