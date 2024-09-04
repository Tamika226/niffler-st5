import os
import datetime

from dotenv import load_dotenv
import pytest
from playwright.sync_api import Playwright, Page, expect, Browser

from databases.auth_db import AuthDb
from databases.spend_db import SpendDb
from models.Config import Envs
from models.Spend import NewSpend, Spend

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


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(
        app_url=os.getenv("APP_URL"),
        auth_url=os.getenv("AUTH_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        spend_db_url=os.getenv("SPEND_DB_URL"),
        userdata_db_url=os.getenv("USERDATA_DB_URL"),
        currency_db_url=os.getenv("CURRENCY_DB_URL"),
        auth_db_url=os.getenv("AUTH_DB_URL"),
        default_timeout=os.getenv("DEFAULT_TIMEOUT"),
        default_user_login=os.getenv("DEFAULT_USER_LOGIN"),
        default_user_password=os.getenv("DEFAULT_USER_PASSWORD")
    )


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


@pytest.fixture
def login(page: Page, identification_page: IdentificationPage, login_page: LoginPage, main_page: MainPage, envs):
    page.goto(envs.app_url)
    identification_page.to_login()

    login_page.enter_username(os.getenv("DEFAULT_USER_LOGIN"))
    login_page.enter_password(os.getenv("DEFAULT_USER_PASSWORD"))
    login_page.click_button()
    expect(main_page.profile).to_be_visible()

    token = page.evaluate("()=>window.sessionStorage.getItem('id_token')")
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
    if categories is None:
        new_name = generator.generate_word()
        categories_client.add_category(new_name)
        return new_name
    return categories[0]["category"]


@pytest.fixture(scope="session")
def get_token(envs):
    auth = AuthClient(envs.auth_url, envs.app_url)
    token = auth.do_login(f"{envs.default_user_login}", f"{envs.default_user_password}")
    return token


@pytest.fixture(scope="session", autouse=True)
def delete_all_spends_after_tests(spends_client):
    yield
    spends = spends_client.get_spends()
    if spends:
        spends_client.remove_spends([spend["id"] for spend in spends])
        assert not spends_client.get_spends()


@pytest.fixture()
def delete_spend(spends_client, id: str):
    spends_client.remove_spends([id])


@pytest.fixture()
def add_spend(spends_client, generator, get_any_category) -> Spend:
    created_spends = []
    def _add_spend(amount: float | None  = None,
                   category: str | None  = None,
                   currency: str | None = "RUB",
                   description: str | None = "",
                   spendDate: str | None = None) -> Spend:

        spend_model = NewSpend(
            amount=amount if amount is not None else generator.generate_amount(),
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
