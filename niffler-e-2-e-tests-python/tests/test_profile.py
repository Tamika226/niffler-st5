from playwright.sync_api import expect


def test_add_category(app, login, generator):
    app.main_page.open_profile()
    category_name = generator.word()

    app.profile_page.enter_category_name(category_name).create_category()

    expect(app.profile_page.created_categories).to_have_text(category_name)
