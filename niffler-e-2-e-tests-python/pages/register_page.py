from playwright.sync_api import Page


class RegisterPage:
    def __init__(self, page: Page):
        self.user_name_input = page.locator('//input[@name="username"]')
        self.password_input = page.locator('//input[@name="password"]')
        self.password_submit = page.locator('//input[@name="passwordSubmit"]')
        self.button = page.locator('//button[@type="submit"]')
        self.error_message = page.locator('//span[@class="form__error"]')
        self.error_username = self.user_name_input.locator('//following-sibling::span[@class="form__error"]')
        self.error_password = self.password_input.locator('//following-sibling::span[@class="form__error"]')
        self.success_registration = page.locator(f'//p[contains(text(), "Congratulations! You\'ve registered!")]')

    def enter_username(self, username: str):
        self.user_name_input.fill(username)
        return self

    def enter_password(self, password: str):
        self.password_input.fill(password)
        return self

    def submit_password(self, password: str):
        self.password_submit.fill(password)
        return self

    def click_submit(self):
        self.button.click()
