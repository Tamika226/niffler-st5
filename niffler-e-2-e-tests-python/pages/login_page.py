from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: 'Page'):
        self.user_name_input = page.locator('//input[@name="username"]')
        self.password_input = page.locator('//input[@name="password"]')
        self.button = page.locator('//button[@type="submit"]')
        self.show_password_button = page.locator('//button[contains(@class,"form__password-button")]')
        self.error_message = page.locator('//p[@class="form__error"]')

    def enter_username(self, username: str):
        self.user_name_input.fill(username)

    def enter_password(self, password: str):
        self.password_input.fill(password)

    def click_button(self):
        self.button.click()

    def show_password(self):
        self.show_password_button.click()


