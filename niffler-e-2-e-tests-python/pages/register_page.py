from playwright.sync_api import Page


class RegisterPage:
    def __init__(self, page: 'Page'):
        self.page = Page
        self.user_name_input = page.locator('//input[@name="username"]')
        self.password_input = page.locator('//input[@name="password"]')
        self.password_submit = page.locator('//input[@name="passwordSubmit"]')
        self.button = page.locator('//button[@type="submit"]')
        self.error_message = page.locator('//span[@class="form__error"]')

    def enter_username(self, username: str):
        self.user_name_input.fill(username)

    def enter_password(self, password: str):
        self.password_input.fill(password)


    def submit_password(self, password: str):
        self.password_submit.fill(password)

    def click_button(self):
        self.button.click()
