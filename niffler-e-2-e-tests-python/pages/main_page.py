from pages.header import Header
from playwright.sync_api import Page


class MainPage(Header):
    def __init__(self, page: 'Page'):
        super().__init__(page)