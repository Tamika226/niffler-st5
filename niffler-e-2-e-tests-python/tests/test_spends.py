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

    expect(main_page.spending_section).to_contain_text(f'{amount}')
    expect(main_page.spending_section).to_contain_text(f'{category_name}')


@Actions.login
def test_type_part_of_category_name(main_page, get_any_category):
    category_name = get_any_category

    main_page.type_category(category_name[:1])
    expect(main_page.category_select.locator(f'//div[contains(text(),"{category_name}")]')).to_be_visible()


@Actions.login
def test_category_non_exists(main_page, generator):

    main_page.type_category(generator.generate_word())

    expect(main_page.category_select.locator(f'//div[contains(text(),"no options")]')).to_be_visible()


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
def test_empty_amount(main_page, get_any_category):

    category_name = get_any_category

    main_page.select_category(category_name)
    main_page.add_new_spend()

    expect(main_page.error_message).to_contain_text("Amount is required")


@Actions.login
def test_empty_spend_date(main_page, generator, get_any_category):

    category_name = get_any_category

    main_page.select_category(category_name)
    main_page.set_amount(str(generator.generate_amount()))
    main_page.type_spend_date("")
    main_page.add_new_spend()

    expect(main_page.error_message).to_contain_text("Spend date is required")


@Actions.login
def test_future_spend_date(main_page, generator, get_any_category):

    category_name = get_any_category

    main_page.select_category(category_name)
    main_page.set_amount(str(generator.generate_amount()))
    main_page.type_spend_date(generator.generate_future_date())
    main_page.add_new_spend()

    expect(main_page.error_message).to_contain_text("You can not pick future date")


@Actions.login
def test_add_wo_description(main_page, generator, get_any_category):
    category_name = get_any_category
    amount = str(generator.generate_amount())

    main_page.select_category(category_name)
    main_page.set_amount(amount)
    main_page.add_new_spend()

    expect(main_page.spending_section).to_contain_text(f'{amount}')
    expect(main_page.spending_section).to_contain_text(f'{category_name}')


@Actions.login
def test_add_with_description_longer_then_256(main_page, generator, get_any_category):
    category_name = get_any_category
    description = generator.generate_string(257)

    main_page.select_category(category_name)
    main_page.set_amount(str(generator.generate_amount()))
    main_page.set_description(description)
    main_page.add_new_spend()
    expect(main_page.spending_section).to_contain_text(f'{description[:255]}')

