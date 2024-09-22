import allure
import pytest
from playwright.sync_api import expect

from helpers.allure_helpers import LoggedExpect
from marks import Actions
from pages.main_page import SpendsHistoryDatesFilter

@allure.epic("e-2-e tests")
@allure.feature("Spends page")
@allure.story("Spends history")
class TestSpendsHistory:
    @Actions.login
    def test_delete_selected_spends_is_disabled(self, main_page):
        LoggedExpect(main_page.spend_history_delete_selected_button).to_be_disabled()

    @Actions.login
    def test_close_filters(self, main_page):
        LoggedExpect(main_page.spend_history_filters_closed).not_to_be_visible()

        main_page.select_currency("RUB")
        LoggedExpect(main_page.spend_history_filters_closed).to_be_visible()

        main_page.close_spend_history_filers()
        LoggedExpect(main_page.spend_history_filters_closed).not_to_be_visible()

    @Actions.login
    def test_delete_selected_spend(self, main_page, add_spend, reload_page):
        spend = add_spend()

        reload_page

        LoggedExpect(main_page.spending_section).to_contain_text(f'{spend.amount:g}')
        LoggedExpect(main_page.spending_section).to_contain_text(f'{spend.category}')

        main_page.select_spend(spend.id)
        main_page.delete_selected_spend()

        LoggedExpect(main_page.spending_section).to_contain_text('No spendings provided yet!')

    @Actions.login
    def test_delete_all_spends(self, main_page, add_spend, reload_page):
        first_spend = add_spend()
        second_spend = add_spend()

        reload_page

        LoggedExpect(main_page.spending_section).to_contain_text(f'{first_spend.amount:g}')
        LoggedExpect(main_page.spending_section).to_contain_text(f'{first_spend.category}')
        LoggedExpect(main_page.spending_section).to_contain_text(f'{second_spend.amount:g}')
        LoggedExpect(main_page.spending_section).to_contain_text(f'{second_spend.category}')

        main_page.select_all_spend()
        main_page.delete_selected_spend()

        LoggedExpect(main_page.spending_section).to_contain_text('No spendings provided yet!')

    @Actions.login
    @pytest.mark.parametrize("period", [SpendsHistoryDatesFilter.Today, SpendsHistoryDatesFilter.LastWeek,
                                        SpendsHistoryDatesFilter.LastMonth])
    def test_filter_by_period(self, main_page, add_spend, generator, reload_page, period):
        spend = add_spend(spendDate=generator.date(period).to_api_format())

        reload_page
        LoggedExpect(main_page.spending_section).to_contain_text(f'{spend.amount:g}')
        LoggedExpect(main_page.spending_section).to_contain_text(f'{spend.category}')

        main_page.select_spends_by_period(period)

        LoggedExpect(main_page.spending_section).to_contain_text('No spendings provided yet!')

    @Actions.login
    def test_filter_all_times_spend(self, main_page, add_spend, reload_page, generator):
        spend = add_spend(spendDate=generator.date(SpendsHistoryDatesFilter.Today).to_api_format())

        reload_page
        LoggedExpect(main_page.spending_section).to_contain_text(f'{spend.amount:g}')
        LoggedExpect(main_page.spending_section).to_contain_text(f'{spend.category}')

        main_page.select_spends_by_period(SpendsHistoryDatesFilter.Today)
        LoggedExpect(main_page.spending_section).to_contain_text('No spendings provided yet!')

        main_page.select_spends_by_period(SpendsHistoryDatesFilter.AllTime)
        LoggedExpect(main_page.spending_section).to_contain_text(f'{spend.amount:g}')
        LoggedExpect(main_page.spending_section).to_contain_text(f'{spend.category}')
