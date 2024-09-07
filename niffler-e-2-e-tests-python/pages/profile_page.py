from pages.header import Header
from playwright.sync_api import Page


class ProfilePage(Header):
    def __init__(self, page: Page):
        super().__init__(page)
        self.category_input = page.locator('//input[@name="category"]')
        self.create_button = page.locator('//button[contains(text(),"Create")]')
        self.created_categories = page.locator('//ul[@class="categories__list"]/child::*[last()]')

    def enter_category_name(self, category: str):
        self.category_input.fill(category)
        return self

    def create_category(self):
        self.create_button.click()

    def get_created_category(self):
        self.created_categories.text_content()
