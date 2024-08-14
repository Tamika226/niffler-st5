from pages.base_page import BasePage
from playwright.sync_api import Page


class MainPage(BasePage):
    def __init__(self, page: 'Page'):
        super().__init__(page)
        self.avatar = page.locator('//img[@class="header__avatar"]')

    def visible_check(self):
        self.avatar.is_visible()


