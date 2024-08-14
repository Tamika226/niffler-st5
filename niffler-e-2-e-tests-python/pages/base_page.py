from playwright.sync_api import Page


class BasePage:

    def __init__(self, page: 'Page'):
        self.page = page
        self.user_name_input = page.locator('//input[@name="username"]')
        self.password_input = page.locator('//input[@name="password"]')
        self.button = page.locator('//button[@type="submit"]')
        self.error_message = page.locator('//span[@class="form__error"]')

    def navigate(self, url):
        self.page.goto(url)

    def enter_username(self, username: str):
        self.user_name_input.fill(username)

    def enter_password(self, password: str):
        self.password_input.fill(password)

    def click_button(self):
        self.button.click()

    def get_error_message(self) -> str:
        return self.error_message.text_content()
