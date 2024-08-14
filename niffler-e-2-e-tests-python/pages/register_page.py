from pages.base_page import BasePage
from playwright.sync_api import Page


class RegisterPage(BasePage):
    def __init__(self, page: 'Page'):
        super().__init__(page)
        self.password_submit = page.locator('//input[@name="passwordSubmit"]')

    def submit_password(self):
        self.password_submit.click()


