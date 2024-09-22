import allure

from pages.header import Header
from playwright.sync_api import Page


class ProfilePage(Header):
    def __init__(self, page: Page):
        super().__init__(page)
        self.category_input = page.locator('//input[@name="category"]')
        self.create_button = page.locator('//button[contains(text(),"Create")]')
        self.created_categories = page.locator('//ul[@class="categories__list"]/child::*[last()]')

    def enter_category_name(self, category: str):
        with (allure.step(f"Вводим название категории = {category}")):
            self.category_input.fill(category)
            return self

    @allure.step("Нажимаем на Кнопку Создать")
    def create_category(self):
        self.create_button.click()

    @allure.step("Получаем название категории")
    def get_created_category(self):
        self.created_categories.text_content()
