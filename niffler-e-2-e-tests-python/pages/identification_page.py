import allure
from playwright.sync_api import Page


class IdentificationPage:
    def __init__(self, page: Page):
        self.login = page.locator('//a[@href="/redirect"]')
        self.registration = page.locator('//a[contains(@href,"register")]')

    @allure.step("Переходим на страницу регистрации")
    def open_registration(self):
        self.registration.click()

    @allure.step("Переходим на страницу авторизации")
    def open_login(self):
        self.login.click()
