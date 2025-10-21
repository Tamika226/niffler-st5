import allure
from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.username_input = page.locator('//input[@name="username"]')
        self.password_input = page.locator('//input[@name="password"]')
        self.button = page.locator('//button[@type="submit"]')
        self.show_password_button = page.locator('//button[contains(@class,"form__password-button")]')
        self.error_message = page.locator('//p[@class="form__error"]')

    def enter_username(self, username: str):
        with (allure.step(f"Вводим имя пользователя = {username}")):
            self.username_input.fill(username)
            return self

    def enter_password(self, password: str):
        with (allure.step(f"Вводим пароль = {password}")):
            self.password_input.fill(password)
            return self

    @allure.step("Нажимаем на кнопку Submit")
    def click_submit(self):
        self.button.click()

    @allure.step("Нажимаем на кнопку Показать пароль")
    def show_password(self):
        self.show_password_button.click()
