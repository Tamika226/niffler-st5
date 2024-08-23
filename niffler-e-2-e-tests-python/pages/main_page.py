from pages.header import Header
from playwright.sync_api import Page


class MainPage(Header):
    def __init__(self, page: 'Page'):
        super().__init__(page)
        self.category_select = page.locator('//form[@class="add-spending__form"]//div[@class="select-wrapper"]')
        self.amount = page.locator('//input[@name="amount"]')
        self.calendar = page.locator('//div[@class="react-datepicker-wrapper"]//input')
        self.description = page.locator('//input[@name="description"]')
        self.add_new_spend_button = page.locator('//button[@type="submit"]')
        self.spending_table = page.locator('//table[@class="table spendings-table"]')
        self.empty_space = page.locator('//div[@class="main-content"]')
        self.error_message = page.locator('//span[@class="form__error"]')

    def select_category(self, category: str):
        self.category_select.click()
        self.category_select.locator(f'//div[contains(text(),"{category}")]').click()

    def set_category(self, category: str):
        self.category_select.click()
        self.category_select.fill(category)
        self.empty_space.click()

    def set_amount(self, amount: str):
        self.amount.fill(amount)
        self.empty_space.click()

    def set_spend_date(self, date: str):
        self.calendar.click()
        self.calendar.clear()
        self.calendar.fill(date)
        self.empty_space.click()

    def set_description(self, description: str):
        self.description.fill(description)

    def add_new_spend(self):
        self.add_new_spend_button.click()

