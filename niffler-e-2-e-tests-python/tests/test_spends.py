from playwright.sync_api import expect
from marks import Actions

@Actions.login
def test_add_spend(main_page, generator, get_any_category):
    category_name = get_any_category
    amount = str(generator.generate_amount())

    main_page.select_category(category_name)
    main_page.set_amount(amount)
    main_page.set_description(generator.generate_word())
    main_page.add_new_spend()

    expect(main_page.spending_table).to_contain_text(f'{amount}')


@Actions.login
def test_category_non_exists(main_page, generator):

    main_page.set_category(generator.generate_word())

    expect(main_page.category_select.locator(f'//div[contains(text(),"no options)]'))


@Actions.login
def test_empty_category(main_page, generator):

    main_page.set_amount(str(generator.generate_amount()))
    main_page.add_new_spend()

    expect(main_page.error_message).to_contain_text("Category is required")


@Actions.login
def test_negative_amount(main_page, generator, get_any_category, envs):

    category_name = get_any_category
    amount = str(-generator.generate_amount())

    main_page.select_category(category_name)
    main_page.set_amount(amount)
    main_page.add_new_spend()

    expect(main_page.error_message).to_contain_text("Amount should be greater than 0")


@Actions.login
def test_empty_amount(main_page, generator, get_any_category):

    category_name = get_any_category

    main_page.select_category(category_name)
    main_page.add_new_spend()

    expect(main_page.error_message).to_contain_text("Amount is required")


@Actions.login
def test_empty_spend_date(main_page, generator, get_any_category):

    category_name = get_any_category

    main_page.select_category(category_name)
    main_page.set_amount(str(generator.generate_amount()))
    main_page.set_spend_date("")
    main_page.add_new_spend()



    expect(main_page.error_message).to_contain_text("Spend date is required")
