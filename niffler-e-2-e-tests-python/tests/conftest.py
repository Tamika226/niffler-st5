import os
import datetime

import allure
import pytest
from allure_commons.reporter import AllureReporter
from allure_commons.types import AttachmentType
from allure_pytest.listener import AllureListener
from dotenv import load_dotenv
from pytest import Item, FixtureDef, FixtureRequest
from playwright.sync_api import Playwright, Page, Browser

from databases.auth_db import AuthDb
from databases.spend_db import SpendDb
from helpers.allure_helpers import LoggedExpect
from models.Config import Envs
from models.Spend import NewSpend, Spend

from helpers.app import App
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.identification_page import IdentificationPage
from pages.register_page import RegisterPage
from pages.profile_page import ProfilePage
from helpers.data_generator import TestDataGenerator

from clients.auth_client import AuthClient
from clients.spends_client import SpendsHttpClient
from clients.categories_client import CategoriesHttpClient

BROWSER = os.getenv('BROWSER') if os.getenv('BROWSER') is not None else 'chrome'
IS_HEADLESS = os.getenv('IS_HEADLESS') if os.getenv('IS_HEADLESS') is not None else False


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_call(item: Item):
    yield
    allure.dynamic.title(" ".join(item.name.split("_")[1:]).title())

def allure_logger(config) -> AllureReporter:
    listener: AllureListener = config.pluginmanager.get_plugin("allure_listener")
    return listener.allure_logger


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
    yield
    logger = allure_logger(request.config)
    item = logger.get_last_item()
    scope_letter = fixturedef.scope[0].upper()
    item.name = f"[{scope_letter}] " + " ".join(fixturedef.argname.split("_")).title()


@pytest.fixture(scope="session")
@allure.title("Environment variables")
def envs() -> Envs:
    load_dotenv()
    envs = Envs(
        app_url=os.getenv("APP_URL"),
        auth_url=os.getenv("AUTH_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        spend_db_url=os.getenv("SPEND_DB_URL"),
        userdata_db_url=os.getenv("USERDATA_DB_URL"),
        currency_db_url=os.getenv("CURRENCY_DB_URL"),
        auth_db_url=os.getenv("AUTH_DB_URL"),
        default_user_login=os.getenv("DEFAULT_USER_LOGIN"),
        default_user_password=os.getenv("DEFAULT_USER_PASSWORD")
    )
    allure.attach(envs.model_dump_json(), name='envs.json', attachment_type=AttachmentType.JSON)
    return envs


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
def reload_page(page: Page):
    page.reload()


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
def login(app, envs):
    app.page.goto(envs.app_url)
    app.identification_page.open_login()

    app.login_page.enter_username(os.getenv("DEFAULT_USER_LOGIN"))
    app.login_page.enter_password(os.getenv("DEFAULT_USER_PASSWORD"))
    app.login_page.click_submit()
    LoggedExpect(app.main_page.profile).to_be_visible()

    token = app.page.evaluate("()=>window.sessionStorage.getItem('id_token')")
    allure.attach(token, name='token.txt', attachment_type=AttachmentType.TEXT)
    return token


@pytest.fixture(scope="session")
def generator():
    generator = TestDataGenerator()
    return generator


@pytest.fixture(scope="session")
def spends_client(envs, get_token) -> SpendsHttpClient:
    return SpendsHttpClient(envs.gateway_url, get_token)


@pytest.fixture(scope="session")
def categories_client(envs, get_token) -> CategoriesHttpClient:
    return CategoriesHttpClient(envs.gateway_url, get_token)


@pytest.fixture()
def get_any_category(categories_client, generator):
    categories = categories_client.get_categories()
    if not categories:
        new_name = generator.word()
        categories_client.add_category(new_name)
        return new_name
    return categories[0]["category"]


@pytest.fixture(scope="session")
def get_token(envs):
    auth = AuthClient(envs.auth_url, envs.app_url)
    token = auth.do_login(f"{envs.default_user_login}", f"{envs.default_user_password}")
    return token


@pytest.fixture(scope="session", autouse=True)
def delete_all_spends_and_categories_after_tests(spends_client, spend_db, categories_client):
    yield
    spends = spends_client.get_spends()
    if spends:
        spends_client.remove_spends([spend["id"] for spend in spends])
        assert not spends_client.get_spends()
    categories = categories_client.get_categories()
    for category in categories:
        spend_db.delete_category(category["id"])



@pytest.fixture()
def add_spend(spends_client, generator, get_any_category) -> Spend:
    created_spends = []
    def _add_spend(amount: float | None  = None,
                   category: str | None  = None,
                   currency: str | None = "RUB",
                   description: str | None = "",
                   spendDate: str | None = None) -> Spend:

        spend_model = NewSpend(
            amount=amount if amount is not None else generator.amount(),
            category=category if category is not None else get_any_category,
            currency=currency,
            description=description,
            spendDate=spendDate if spendDate is not None else str((datetime.datetime.utcnow() - datetime.timedelta(days=1)).isoformat())
        )

        spend = spends_client.add_spends(spend_model)
        created_spends.append(spend)
        return spend

    yield _add_spend
    spends_client.remove_spends([created_spend.id for created_spend in created_spends])


@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDb:
    return SpendDb(envs.spend_db_url)


@pytest.fixture(scope="session")
def auth_db(envs) -> AuthDb:
    return AuthDb(envs.auth_db_url)


@pytest.fixture()
def check_user_in_db(auth_db):
    def _check_user_in_db(username: str):
        user = auth_db.get_user(username)
        return True if user else False
    return _check_user_in_db


@pytest.fixture(scope="session", autouse=True)
def delete_all_users_except_test_after_all(auth_db, envs):
    users = auth_db.get_all_users()
    for user in users:
        if user.username != envs.default_user_login:
            auth_db.delete_user(user.username)
