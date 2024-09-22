import allure

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
    def __init__(self, page: Page):
        super().__init__(page)
        self.category_select = page.locator('//form[@class="add-spending__form"]//div[@class="select-wrapper"]')
        self.category_selector_without_coincidence = self.category_select.locator('//div[contains(text(),"No options")]')
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


    def type_category(self, category: str):
        with (allure.step(f"Печатаем в поле категорию = {category} и нажимаем на нее")):
            self.category_select.click()
            self.category_select.type(category)

    def get_category_in_list_by_name(self, category_name: str):
        with (allure.step(f"Получаем локатор категории = {category_name}")):
            return self.category_select.locator(f'//div[contains(text(),"{category_name}")]')

    def select_category(self, category: str):
        with (allure.step(f"Выбираем из списка категорию = {category}")):
            self.category_select.click()
            self.get_category_in_list_by_name(category).click()
            return self

    def set_amount(self, amount: str):
        with (allure.step(f"Вводим сумму = {amount}")):
            self.amount.fill(amount)
            self.empty_space.click()
            return self

    def type_spend_date(self, date: str):
        with (allure.step(f"Вводим дату траты = {date}")):
            self.calendar.click()
            self.calendar.clear()
            self.calendar.type(date)
            self.empty_space.click()
            return self

    def set_description(self, description: str):
        with (allure.step(f"Вводим описание траты = {description}")):
            self.description.fill(description)
            return self

    def type_description(self, description: str):
        with (allure.step(f"Печатаем описание даты посимвольно = {description}")):
            self.description.type(description)
            return self

    @allure.step("Нажимаем на кнопку Добавить трату")
    def add_new_spend(self):
        self.add_new_spend_button.click()

    def select_spend(self, spend_id:str):
        with (allure.step(f"Выбираем трату с id = {spend_id} из истории трат")):
            self.spending_section.locator(f'//td/input[@value="{spend_id}"]').click()
            return self

    @allure.step("Нажимаем на чекбокс Выбрать все траты")
    def select_all_spend(self):
        self.all_spends_checkbox.click()

    @allure.step("Нажимаем на кнопку Удалить выбранные траты")
    def delete_selected_spend(self):
        self.spend_history_delete_selected_button.click()

    def select_currency(self, currency_name:str):
        with (allure.step(f"Выбираем валюту траты = {currency_name} в истории трат")):
            self.spend_history_currency_wrapper.click()
            self.spend_history_currency_wrapper.locator(f'//div[contains(text(),"{currency_name}")]').click()
            return self

    @allure.step("Нажимаем на кнопку удалить выбранные фильтры истории трат ")
    def close_spend_history_filers(self):
        self.spend_history_filters_closed.click()

    def select_spends_by_period(self, period: SpendsHistoryDatesFilter):
        with (allure.step(f"Выбираем траты за период = {SpendsHistoryDatesFilter.name} в истории трат")):
            self.spending_section.locator(f'//button[contains(text(),"{StringHelper.camel_to_sentence(period.name)}")]').click()
            return self
