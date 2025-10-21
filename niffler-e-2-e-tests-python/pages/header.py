import allure
from playwright.sync_api import Page
from enum import Enum


class Header:

    def __init__(self, page: Page):
        self.profile = page.locator('//a[@href="/profile"]')
        self.people = page.locator('//a[@href="/people"]')
        self.friends = page.locator('//a[@href="/friends"]')
        self.main = page.locator('//a[@href="/main"]')

    @allure.step("Переходим на страницу профиля")
    def open_profile(self):
        self.profile.click()

    @allure.step("Переходим на страницу всех пользователей")
    def open_people(self):
        self.profile.click()

    @allure.step("Переходим на страницу друзей")
    def open_friends(self):
        self.friends.click()

    @allure.step("Переходим на главную страницу")
    def open_main(self):
        self.main.click()


class CurrencyTypes(Enum):
    RUB = 1
    KZT = 2
    EUR = 3
    USD = 4
