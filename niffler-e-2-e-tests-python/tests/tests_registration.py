import pytest
from playwright.sync_api import expect


def test_success_registration(page, identification_page, register_page, envs, generator, check_user_in_db):
    page.goto(envs.app_url)
    identification_page.to_registration()

    username = generator.generate_name()
    password = generator.generate_password()

    register_page.enter_username(username)
    register_page.enter_password(password)
    register_page.submit_password(password)

    register_page.click_button()

    expect(register_page.success_registration).to_be_visible()
    assert check_user_in_db(username) is not None


def test_registration_existing_user(page, identification_page, register_page, envs, generator):
    page.goto(envs.app_url)
    identification_page.to_registration()

    register_page.enter_username(envs.default_user_login)
    register_page.enter_password(envs.default_user_password)
    register_page.submit_password(envs.default_user_password)

    register_page.click_button()

    expect(register_page.error_message).to_have_text(f'Username `{envs.default_user_login}` already exists')


def test_registration_with_different_passwords(page, identification_page, register_page, envs, generator, check_user_in_db):
    page.goto(envs.app_url)
    identification_page.to_registration()

    username = generator.generate_name()

    register_page.enter_username(username)
    register_page.enter_password(generator.generate_password())
    register_page.submit_password(generator.generate_password())

    register_page.click_button()

    expect(register_page.error_password).to_have_text('Passwords should be equal')
    assert check_user_in_db(username) is None


@pytest.mark.parametrize("name_length", [2, 51])
def test_registration_with_inappropriate_name_length(page, identification_page, register_page, envs, generator, check_user_in_db, name_length):
    page.goto(envs.app_url)
    identification_page.to_registration()

    username = generator.generate_string(name_length)

    register_page.enter_username(username)
    register_page.enter_password(generator.generate_password())
    register_page.submit_password(generator.generate_password())

    register_page.click_button()

    expect(register_page.error_username).to_have_text('Allowed username length should be from 3 to 50 characters')
    assert check_user_in_db(username) is None


@pytest.mark.parametrize("password_length", [2, 13])
def test_registration_with_inappropriate_password_length(page, identification_page, register_page, envs, generator, check_user_in_db, password_length):
    page.goto(envs.app_url)
    identification_page.to_registration()

    username = generator.generate_name()
    password = generator.generate_string(password_length)

    register_page.enter_username(username)
    register_page.enter_password(password)
    register_page.submit_password(password)

    register_page.click_button()

    expect(register_page.error_password).to_have_text('Allowed password length should be from 3 to 12 characters')
    assert check_user_in_db(username) is None



