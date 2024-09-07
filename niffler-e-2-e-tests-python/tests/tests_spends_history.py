from playwright.sync_api import expect
from marks import Actions
from datetime import datetime, timedelta
from pages.main_page import SpendsHistoryDatesFilter


class TestSpendHistory:
    @Actions.login
    def test_delete_selected_spends_is_disabled(self, main_page):
        expect(main_page.spend_history_delete_selected_button).to_be_disabled()

    @Actions.login
    def test_close_filters(self, main_page):
        expect(main_page.spend_history_filters_closed).not_to_be_visible()

        main_page.select_currency("RUB")
        expect(main_page.spend_history_filters_closed).to_be_visible()

        main_page.close_spend_history_filers()
        expect(main_page.spend_history_filters_closed).not_to_be_visible()

    @Actions.login
    def test_delete_selected_spend(self, main_page, add_spend, reload_page):
        spend = add_spend()

        reload_page
        expect(main_page.spending_section).to_contain_text(f'{spend.amount:g}')
        expect(main_page.spending_section).to_contain_text(f'{spend.category}')

        main_page.select_spend(spend.id)
        main_page.delete_selected_spend()

        expect(main_page.spending_section).to_contain_text('No spendings provided yet!')

    @Actions.login
    def test_delete_all_spends(self, main_page, add_spend, reload_page):
        first_spend = add_spend()
        second_spend = add_spend()

        reload_page
        expect(main_page.spending_section).to_contain_text(f'{first_spend.amount:g}')
        expect(main_page.spending_section).to_contain_text(f'{first_spend.category}')
        expect(main_page.spending_section).to_contain_text(f'{second_spend.amount:g}')
        expect(main_page.spending_section).to_contain_text(f'{second_spend.category}')

        main_page.select_all_spend()
        main_page.delete_selected_spend()

        expect(main_page.spending_section).to_contain_text('No spendings provided yet!')

    @Actions.login
    def test_filter_today_spend(self, main_page, add_spend, reload_page):
        spend_date = str((datetime.utcnow() - timedelta(days=2)).isoformat())
        spend = add_spend(spendDate=spend_date)
        reload_page
        expect(main_page.spending_section).to_contain_text(f'{spend.amount:g}')
        expect(main_page.spending_section).to_contain_text(f'{spend.category}')

        main_page.select_spends_by_period(SpendsHistoryDatesFilter.Today)

        expect(main_page.spending_section).to_contain_text('No spendings provided yet!')

    @Actions.login
    def test_filter_last_week_spend(self, main_page, add_spend, reload_page):
        spend_date = str((datetime.utcnow() - timedelta(days=8)).isoformat())
        spend = add_spend(spendDate=spend_date)
        reload_page
        expect(main_page.spending_section).to_contain_text(f'{spend.amount:g}')
        expect(main_page.spending_section).to_contain_text(f'{spend.category}')

        main_page.select_spends_by_period(SpendsHistoryDatesFilter.LastWeek)

        expect(main_page.spending_section).to_contain_text('No spendings provided yet!')

    @Actions.login
    def test_filter_last_month_spend(self, main_page, add_spend, reload_page):
        spend_date = str((datetime.utcnow() - timedelta(days=41)).isoformat())
        spend = add_spend(spendDate=spend_date)
        reload_page
        expect(main_page.spending_section).to_contain_text(f'{spend.amount:g}')
        expect(main_page.spending_section).to_contain_text(f'{spend.category}')

        main_page.select_spends_by_period(SpendsHistoryDatesFilter.LastMonth)

        expect(main_page.spending_section).to_contain_text('No spendings provided yet!')

    @Actions.login
    def test_filter_all_times_spend(self, main_page, add_spend, reload_page):
        spend_date = str((datetime.utcnow() - timedelta(days=2)).isoformat())
        spend = add_spend(spendDate=spend_date)
        reload_page
        expect(main_page.spending_section).to_contain_text(f'{spend.amount:g}')
        expect(main_page.spending_section).to_contain_text(f'{spend.category}')

        main_page.select_spends_by_period(SpendsHistoryDatesFilter.Today)
        expect(main_page.spending_section).to_contain_text('No spendings provided yet!')

        main_page.select_spends_by_period(SpendsHistoryDatesFilter.AllTime)
        expect(main_page.spending_section).to_contain_text(f'{spend.amount:g}')
        expect(main_page.spending_section).to_contain_text(f'{spend.category}')
