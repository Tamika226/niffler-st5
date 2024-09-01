from pages.header import Header
from playwright.sync_api import Page
from enum import Enum
from helpers.string_helper import StringHelper


class SpendsHistoryDatesFilter(Enum):
    Today = 1
    LastWeek = 2
    LastMonth = 3
    AllTime = 4


class MainPage(Header):
    def __init__(self, page: 'Page'):
        super().__init__(page)
        self.category_select = page.locator('//form[@class="add-spending__form"]//div[@class="select-wrapper"]')
        self.amount = page.locator('//input[@name="amount"]')
        self.calendar = page.locator('//div[@class="react-datepicker-wrapper"]//input')
        self.description = page.locator('//input[@name="description"]')
        self.add_new_spend_button = page.locator('//button[@type="submit"]')
        self.error_message = page.locator('//span[@class="form__error"]')
        self.empty_space = page.locator('//div[@class="main-content"]')

        self.spending_section = page.locator('//section[@class="main-content__section main-content__section-history"]')
        self.all_spends_checkbox = self.spending_section.locator('//th/input[@type="checkbox"]')
        self.spend_history_delete_selected_button = self.spending_section.locator('//button[contains(text(),"Delete selected")]')

        self.spend_history_currency_wrapper = self.spending_section.locator('//div[@class="select-wrapper"]')
        self.spend_history_filters_closed = self.spending_section.locator('//button[@class="button-icon button-icon_type_close"]')

    def select_category(self, category: str):
        self.category_select.click()
        self.category_select.locator(f'//div[contains(text(),"{category}")]').click()

    def type_category(self, category: str):
        self.category_select.click()
        self.category_select.type(category)

    def set_amount(self, amount: str):
        self.amount.fill(amount)
        self.empty_space.click()

    def type_spend_date(self, date: str):
        self.calendar.click()
        self.calendar.clear()
        self.calendar.type(date)
        self.empty_space.click()

    def set_description(self, description: str):
        self.description.fill(description)

    def type_description(self, description: str):
        self.description.type(description)

    def add_new_spend(self):
        self.add_new_spend_button.click()

    def select_spend(self, spend_id:str):
        self.spending_section.locator(f'//td/input[@value="{spend_id}"]').click()

    def select_all_spend(self):
        self.all_spends_checkbox.click()

    def delete_selected_spend(self):
        self.spend_history_delete_selected_button.click()

    def select_currency(self, currency_name:str):
        self.spend_history_currency_wrapper.click()
        self.spend_history_currency_wrapper.locator(f'//div[contains(text(),"{currency_name}")]').click()

    def close_spend_history_filers(self):
        self.spend_history_filters_closed.click()

    def select_spends_by_period(self, period: SpendsHistoryDatesFilter):
        self.spending_section.locator(f'//button[contains(text(),"{StringHelper.camel_to_sentence(period.name)}")]').click()
