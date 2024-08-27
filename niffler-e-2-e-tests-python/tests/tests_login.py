from playwright.sync_api import expect

import os


def test_success_login(page, identification_page, login_page, main_page, envs):
    page.goto(envs.app_url)
    identification_page.to_login()

    login_page.enter_username(os.getenv("DEFAULT_USER_LOGIN"))
    login_page.enter_password(os.getenv("DEFAULT_USER_PASSWORD"))
    login_page.click_button()

    expect(main_page.profile).to_be_visible()


def test_incorrect_password(page, identification_page, login_page, envs, generator):
    page.goto(envs.app_url)
    identification_page.to_login()

    login_page.enter_username(generator.generate_name())
    login_page.enter_password(generator.generate_password())
    login_page.click_button()

    expect(login_page.error_message).to_contain_text("Неверные учетные данные пользователя")


def test_show_password(page, identification_page, login_page, envs, generator):
    page.goto(envs.app_url)
    identification_page.to_login()

    generated_password = generator.generate_password()
    login_page.enter_password(generated_password)
    expect(login_page.password_input).to_have_attribute('type', 'password')

    login_page.show_password()

    expect(login_page.password_input).to_have_attribute('type', 'text')
    expect(login_page.password_input).to_have_value(generated_password)
