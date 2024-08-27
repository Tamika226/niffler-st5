import os

import allure
import pytest
from allure_commons.reporter import AllureReporter
from allure_commons.types import AttachmentType
from allure_pytest.listener import AllureListener
from dotenv import load_dotenv
from pytest import Item, FixtureDef, FixtureRequest
from playwright.sync_api import Playwright, Page, expect, Browser

from models.config import Envs
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


def allure_logger(config) -> AllureReporter:
    listener: AllureListener = config.pluginmanager.get.plugin("allure_listener")
    return listener.allure_logger


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_call(item: Item):
    yield
    allure.dynamic.title(" ".join(item.name.split("_")[1:]).title())


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_call(fixturedef: FixtureDef, request: FixtureRequest):
    yield
    logger = allure_logger(request.config)
    item = logger.get_last_item()
    scope_letter = fixturedef.scope[0].upper()
    item.name = f"[{scope_letter}]" + " ".join(fixturedef.argname.split("_")).title()


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    envs = Envs(
        app_url=os.getenv("APP_URL"),
        auth_url=os.getenv("AUTH_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        default_timeout=os.getenv("DEFAULT_TIMEOUT"),
        default_user_login=os.getenv("DEFAULT_USER_LOGIN"),
        default_user_password=os.getenv("DEFAULT_USER_PASSWORD")
    )
    allure.attach(envs, name='envs.json', attachment_type=AttachmentType.JSON)
    return envs


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
def page(browser: Browser, envs) -> Page:
    page = browser.new_page()
    page.set_default_timeout(envs.default_timeout)
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
def login(page: Page, identification_page: IdentificationPage, login_page: LoginPage, main_page: MainPage, envs):
    page.goto(envs.app_url)
    identification_page.to_login()

    login_page.enter_username(os.getenv("DEFAULT_USER_LOGIN"))
    login_page.enter_password(os.getenv("DEFAULT_USER_PASSWORD"))
    login_page.click_button()
    expect(main_page.profile).to_be_visible()

    token = page.evaluate("()=>window.sessionStorage.getItem('id_token')")
    allure.attach(token, name='token.txt', attachment_type=AttachmentType.TEXT)
    return token


@pytest.fixture(scope="session")
def generator():
    generator = TestDataGenerator()
    return generator


@pytest.fixture()
def spends_client(envs, login) -> SpendsHttpClient:
    return SpendsHttpClient(envs.gateway_url, login)


@pytest.fixture()
def categories_client(envs, login) -> CategoriesHttpClient:
    return CategoriesHttpClient(envs.gateway_url, login)


@pytest.fixture()
def get_any_category(categories_client, generator):
    categories = categories_client.get_categories()
    if categories is None:
        new_name = generator.generate_word()
        categories_client.add_category(new_name)
        return new_name
    return categories[0]["category"]
