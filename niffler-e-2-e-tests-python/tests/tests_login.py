from playwright.sync_api import expect


class TestLogin:
    def test_success_login(self, app, envs):
        app.page.goto(envs.app_url)
        app.identification_page.open_login()

        app.login_page.enter_username(envs.default_user_login).enter_password(envs.default_user_password).click_submit()

        expect(app.main_page.profile).to_be_visible()

    def test_incorrect_password(self, app, envs, generator):
        app.page.goto(envs.app_url)
        app.identification_page.open_login()

        app.login_page.enter_username(generator.name()).enter_password(generator.password()).click_submit()

        expect(app.login_page.error_message).to_contain_text("Неверные учетные данные пользователя")

    def test_show_password(self, app, envs, generator):
        app.page.goto(envs.app_url)
        app.identification_page.open_login()

        generated_password = generator.password()

        app.login_page.enter_password(generated_password)

        expect(app.login_page.password_input).to_have_attribute('type', 'password')

        app.login_page.show_password()

        expect(app.login_page.password_input).to_have_attribute('type', 'text')
        expect(app.login_page.password_input).to_have_value(generated_password)

