from pages.login_page import LoginPage
from pages.main_page import MainPage
import os


def test1(page):
    login_page = LoginPage(page)
    login_page.navigate(os.getenv("AUTH_URL"))
    login_page.enter_username('test')
    login_page.enter_password('12345')
    login_page.click_button()
    main_page = MainPage(page)
    main_page.visible_check()
    assert True
