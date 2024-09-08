import allure
import pytest
from playwright.sync_api import expect


class TestRegistration:
    def test_success_registration(self, app, envs, generator, check_user_in_db):
        app.page.goto(envs.app_url)
        app.identification_page.open_registration()

        username = generator.name()
        password = generator.password()

        app.register_page.enter_username(username).enter_password(password).submit_password(password).click_submit()

        expect(app.register_page.success_registration).to_be_visible()
        assert check_user_in_db(username)

    def test_registration_existing_user(self, app, envs, generator):
        app.page.goto(envs.app_url)
        app.identification_page.open_registration()

        app.register_page.enter_username(envs.default_user_login).enter_password(
            envs.default_user_password).submit_password(envs.default_user_password).click_submit()

        expect(app.register_page.error_message).to_have_text(f'Username `{envs.default_user_login}` already exists')

    def test_registration_with_different_passwords(self, app, envs, generator,
                                                   check_user_in_db):
        app.page.goto(envs.app_url)
        app.identification_page.open_registration()

        username = generator.name()

        app.register_page.enter_username(username).enter_password(generator.password()).submit_password(
            generator.password()).click_submit()

        expect(app.register_page.error_password).to_have_text('Passwords should be equal')
        assert not check_user_in_db(username)

    @pytest.mark.parametrize("name_length", [2, 51])
    def test_registration_with_inappropriate_name_length(self, app, envs, generator,
                                                         check_user_in_db, name_length):
        app.page.goto(envs.app_url)
        app.identification_page.open_registration()

        username = generator.string(name_length)

        app.register_page.enter_username(username).enter_password(generator.password()).submit_password(
            generator.password()).click_submit()

        expect(app.register_page.error_username).to_have_text('Allowed username length should be from 3 to 50 characters')
        assert not check_user_in_db(username)

    @pytest.mark.parametrize("password_length", [2, 13])
    def test_registration_with_inappropriate_password_length(self, app, envs, generator,
                                                             check_user_in_db, password_length):
        app.page.goto(envs.app_url)
        app.identification_page.open_registration()

        username = generator.name()
        password = generator.string(password_length)

        app.register_page.enter_username(username).enter_password(password).submit_password(password).click_submit()

        expect(app.register_page.error_password).to_have_text('Allowed password length should be from 3 to 12 characters')
        assert not check_user_in_db(username)
