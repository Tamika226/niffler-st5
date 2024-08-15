from playwright.sync_api import Page


class Header:

    def __init__(self, page: 'Page'):
        self.profile = page.locator('//a[@href="/profile"]')
        self.people = page.locator('//a[@href="/people"]')
        self.friends = page.locator('//a[@href="/friends"]')
        self.main = page.locator('//a[@href="/main"]')

    def to_profile(self):
        self.profile.click()

    def to_people(self):
        self.profile.click()

    def to_friends(self):
        self.friends.click()

    def to_main(self):
        self.main.click()

