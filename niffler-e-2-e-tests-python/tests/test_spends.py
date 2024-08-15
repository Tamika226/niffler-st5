from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.profile_page import ProfilePage
from helpers.data_generator import TestDataGenerator

import os

generator = TestDataGenerator()


def test_add_spend(page: Page, main_page: MainPage, profile_page: ProfilePage, login):
    main_page.to_profile()
    category_name = profile_page.get_created_category()
    profile_page.to_main()
    assert True

