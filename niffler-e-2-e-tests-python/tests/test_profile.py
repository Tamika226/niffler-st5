from playwright.sync_api import expect

from helpers.allure_helpers import LoggedExpect
from marks import Actions


class TestProfile:
    @Actions.login
    def test_add_category(self, app, login, generator):
        app.main_page.open_profile()
        category_name = generator.word()

        app.profile_page.enter_category_name(category_name).create_category()

        LoggedExpect(app.profile_page.created_categories).to_contain_text(category_name)
