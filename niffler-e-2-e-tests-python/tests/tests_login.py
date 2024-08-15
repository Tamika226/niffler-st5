from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.identification_page import IdentificationPage
from helpers.data_generator import TestDataGenerator

import os

generator = TestDataGenerator()


def test_success_login(page: Page, identification_page: IdentificationPage, login_page: LoginPage, main_page: MainPage, app_url):
    page.goto(app_url)
    identification_page.to_login()

    login_page.enter_username(os.getenv("DEFAULT_USER_LOGIN"))
    login_page.enter_password(os.getenv("DEFAULT_USER_PASSWORD"))
    login_page.click_button()

    expect(main_page.profile).to_be_visible()


def test_incorrect_password(page: Page, identification_page: IdentificationPage, login_page: LoginPage, main_page: MainPage, app_url):
    page.goto(app_url)
    identification_page.to_login()

    login_page.enter_username(generator.generate_name())
    login_page.enter_password(generator.generate_password())
    login_page.click_button()

    expect(login_page.error_message).to_contain_text("Неверные учетные данные пользователя")
