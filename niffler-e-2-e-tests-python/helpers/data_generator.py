import string

from faker import Faker
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random


class TestDataGenerator:

    one_period = 1

    def __init__(self):
        self.fake = Faker()

    def name(self):
        return self.fake.name()

    def password(self, length=10):
        return self.fake.password(length=length, special_chars=True, digits=True, upper_case=True, lower_case=True)

    def word(self):
        return self.fake.word()

    def amount(self):
        return str(self.fake.random_int(min=1, max=100))

    def date(self):
        return f"{self.fake.date_time(): %d/%m/%Y}"

    @staticmethod
    def future_date():
        future_date = datetime.now() + relativedelta(years=1)
        return f"{future_date: %d/%m/%Y}"

    @staticmethod
    def generate_string(size: int):
        return ''.join(random.choices(string.ascii_letters, k=size))
