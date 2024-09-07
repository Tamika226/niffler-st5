from playwright.sync_api import expect
from marks import Actions


@Actions.login
def test_add_spend(app, generator, get_any_category):
    category_name = get_any_category
    amount = generator.amount()

    app.main_page.select_category(category_name).set_amount(amount).set_spend_date(generator.date()).set_description(
        generator.word()).add_new_spend()

    expect(app.main_page.spending_section).to_contain_text(f'{amount}')
    expect(app.main_page.spending_section).to_contain_text(f'{category_name}')


@Actions.login
def test_type_part_of_category_name(app, generator, get_any_category):
    category_name = get_any_category

    app.main_page.type_category(category_name[:1])
    expect(app.main_page.category_select.locator(f'//div[contains(text(),"{category_name}")]')).to_be_visible()


@Actions.login
def test_category_non_exists(app, generator):
    app.main_page.set_category(generator.word())
    expect(app.main_page.category_selector_without_coincidence).to_be_visible()


@Actions.login
def test_empty_category(app, login, generator):
    app.main_page.set_amount(str(generator.amount())).add_new_spend()

    expect(app.main_page.error_message).to_contain_text("Category is required")


@Actions.login
def test_negative_amount(app, generator, get_any_category):
    category_name = get_any_category

    app.main_page.select_category(category_name).set_amount("-" + generator.amount()).add_new_spend()

    expect(app.main_page.error_message).to_contain_text("Amount should be greater than 0")


@Actions.login
def test_empty_amount(app, generator, get_any_category):
    category_name = get_any_category

    app.main_page.select_category(category_name).add_new_spend()

    expect(app.main_page.error_message).to_contain_text("Amount is required")


@Actions.login
def test_empty_spend_date(app, generator, get_any_category):
    category_name = get_any_category

    app.main_page.select_category(category_name).set_amount(generator.amount()).set_spend_date("").add_new_spend()

    expect(app.main_page.error_message).to_contain_text("Spend date is required")


@Actions.login
def test_future_spend_date(app, generator, get_any_category):
    category_name = get_any_category

    app.main_page.select_category(category_name).set_amount(generator.amount()).set_spend_date(
        generator.future_date()).add_new_spend()

    expect(app.main_page.error_message).to_contain_text("You can not pick future date")


@Actions.login
def test_add_wo_description(app, generator, get_any_category):
    category_name = get_any_category
    amount = str(generator.generate_amount())

    app.main_page.select_category(category_name).set_amount(generator.amount()).add_new_spend()

    expect(app.main_page.spending_section).to_contain_text(f'{amount}')
    expect(app.main_page.spending_section).to_contain_text(f'{category_name}')


@Actions.login
def test_add_with_description_longer_then_256(app, generator, get_any_category):
    category_name = get_any_category
    description = generator.generate_string(257)

    app.main_page.select_category(category_name).set_amount(generator.amount()).set_description(
        description).add_new_spend()

    expect(app.main_page.spending_section).to_contain_text(f'{description[:255]}')
