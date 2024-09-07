import string

from faker import Faker
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random
from pages.main_page import SpendsHistoryDatesFilter


class TestDataGenerator:
    two_periods = 2

    def __init__(self):
        self.fake = Faker()
        self.result_date = None

    def name(self):
        return self.fake.name()

    def password(self, length=10):
        return self.fake.password(length=length, special_chars=True, digits=True, upper_case=True, lower_case=True)

    def word(self):
        return self.fake.word()

    def amount(self):
        return str(self.fake.random_int(min=1, max=100))

    @staticmethod
    def generate_string(size: int):
        return ''.join(random.choices(string.ascii_letters, k=size))

    def date(self, period):

        current_date = datetime.now()

        if period == SpendsHistoryDatesFilter.Today:
            self.result_date = current_date - timedelta(days=self.two_periods)
        elif period == SpendsHistoryDatesFilter.LastWeek:
            self.result_date = current_date - timedelta(weeks=self.two_periods)
        elif period == SpendsHistoryDatesFilter.LastMonth:
            self.result_date = current_date - relativedelta(month=self.two_periods)
        else:
            self.result_date = datetime.now() + timedelta(days=self.two_periods)

        return self

    def to_input_format(self):
        return f"{self.result_date: %d/%m/%Y}"

    def to_api_format(self):
        return str(self.result_date.isoformat())


