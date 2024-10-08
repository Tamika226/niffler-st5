from playwright.sync_api import expect


def test_add_spend(app, login, generator, get_any_category):
    category_name = get_any_category
    amount = generator.amount()

    app.main_page.select_category(category_name).set_amount(amount).set_spend_date(generator.date()).set_description(
        generator.word()).add_new_spend()

    expect(app.main_page.spending_table.locator(f'text="{amount}'))


def test_category_non_exists(app, login, generator):
    app.main_page.set_category(generator.word())

    expect(app.main_page.category_selector_without_coincidence).to_be_visible()


def test_empty_category(app, login, generator):
    app.main_page.set_amount(str(generator.amount())).add_new_spend()

    expect(app.main_page.error_message).to_contain_text("Category is required")


def test_negative_amount(app, login, generator, get_any_category):
    category_name = get_any_category

    app.main_page.select_category(category_name).set_amount("-" + generator.amount()).add_new_spend()

    expect(app.main_page.error_message).to_contain_text("Amount should be greater than 0")


def test_empty_amount(app, login, generator, get_any_category):
    category_name = get_any_category

    app.main_page.select_category(category_name).add_new_spend()

    expect(app.main_page.error_message).to_contain_text("Amount is required")


def test_empty_spend_date(app, login, generator, get_any_category):
    category_name = get_any_category

    app.main_page.select_category(category_name).set_amount(generator.amount()).set_spend_date("").add_new_spend()

    expect(app.main_page.error_message).to_contain_text("Spend date is required")
