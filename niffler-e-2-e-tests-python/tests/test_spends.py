from playwright.sync_api import Page, expect
from pages.main_page import MainPage
from pages.profile_page import ProfilePage


def test_add_spend(page: Page, main_page: MainPage, profile_page: ProfilePage, login, generator, get_any_category, spends_client):
    category_name = get_any_category
    amount = str(generator.generate_amount())

    main_page.select_category(category_name)
    main_page.set_amount(amount)
    main_page.set_spend_date(generator.generate_date())
    main_page.set_description(generator.generate_word())
    main_page.add_new_spend()

    expect(main_page.spending_table.locator(f'text="{amount}'))


def test_category_non_exists(page: Page, main_page: MainPage, profile_page: ProfilePage, login, generator, get_any_category, spends_client):

    main_page.set_category(generator.generate_word())

    expect(main_page.category_select.locator(f'//div[contains(text(),"no options)]'))


def test_empty_category(page: Page, main_page: MainPage, profile_page: ProfilePage, login, generator, get_any_category, spends_client):

    main_page.set_amount(str(generator.generate_amount()))
    main_page.add_new_spend()

    expect(main_page.error_message).to_contain_text("Category is required")


def test_negative_amount(page: Page, main_page: MainPage, profile_page: ProfilePage, login, generator, get_any_category, spends_client):

    category_name = get_any_category
    amount = str(-generator.generate_amount())

    main_page.select_category(category_name)
    main_page.set_amount(amount)
    main_page.add_new_spend()

    expect(main_page.error_message).to_contain_text("Amount should be greater than 0")


def test_empty_amount(page: Page, main_page: MainPage, profile_page: ProfilePage, login, generator, get_any_category, spends_client):

    category_name = get_any_category

    main_page.select_category(category_name)
    main_page.add_new_spend()

    expect(main_page.error_message).to_contain_text("Amount is required")


def test_empty_spend_date(page: Page, main_page: MainPage, profile_page: ProfilePage, login, generator, get_any_category, spends_client):

    category_name = get_any_category

    main_page.select_category(category_name)
    main_page.set_amount(str(generator.generate_amount()))
    main_page.set_spend_date("")
    main_page.add_new_spend()

    expect(main_page.error_message).to_contain_text("Spend date is required")
