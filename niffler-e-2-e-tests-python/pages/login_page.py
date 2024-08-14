from pages.base_page import BasePage
from playwright.sync_api import Page


class LoginPage(BasePage):
    def __init__(self, page: 'Page'):
        super().__init__(page)

