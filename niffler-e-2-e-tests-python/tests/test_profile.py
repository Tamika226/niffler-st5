from playwright.sync_api import expect

from marks import Actions


@Actions.login
def test_add_category(main_page, profile_page, generator):
    main_page.to_profile()
    category_name = generator.generate_word()

    profile_page.enter_category_name(category_name)
    profile_page.create_category()

    expect(profile_page.created_categories).to_have_text(category_name)
