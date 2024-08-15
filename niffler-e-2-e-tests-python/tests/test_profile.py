from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.profile_page import ProfilePage
from helpers.data_generator import TestDataGenerator

import os

generator = TestDataGenerator()


def test_add_category(page: Page, main_page: MainPage, profile_page: ProfilePage, login):
    main_page.to_profile()
    category_name = generator.generate_word()

    profile_page.enter_category_name(category_name)
    profile_page.create_category()

    expect(profile_page.created_categories).to_have_text(category_name)


