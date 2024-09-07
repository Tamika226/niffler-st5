from playwright.sync_api import Page


class IdentificationPage:
    def __init__(self, page: 'Page'):
        self.login = page.locator('//a[@href="/redirect"]')
        self.registration = page.locator('//a[contains(@href,"register")]')

    def to_registration(self):
        self.registration.click()

    def to_login(self):
        self.login.click()
