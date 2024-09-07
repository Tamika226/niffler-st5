from playwright.sync_api import Page, expect

import os


def test_success_login(app, app_url):
    app.page.goto(app_url)
    app.identification_page.open_login()

    app.login_page.enter_username(os.getenv("DEFAULT_USER_LOGIN")).enter_password(os.getenv("DEFAULT_USER_PASSWORD")).click_submit()

    expect(app.main_page.profile).to_be_visible()


def test_incorrect_password(app, app_url, generator):
    app.page.goto(app_url)
    app.identification_page.open_login()

    app.login_page.enter_username(generator.name()).enter_password(generator.password()).click_submit()

    expect(app.login_page.error_message).to_contain_text("Неверные учетные данные пользователя")


def test_show_password(app, app_url, generator):
    app.page.goto(app_url)
    app.identification_page.open_login()

    generated_password = generator.password()

    app.login_page.enter_password(generated_password)

    expect(app.login_page.password_input).to_have_attribute('type', 'password')

    app.login_page.show_password()

    expect(app.login_page.password_input).to_have_attribute('type', 'text')
    expect(app.login_page.password_input).to_have_value(generated_password)
