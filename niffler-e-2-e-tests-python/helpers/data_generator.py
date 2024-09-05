import string

from faker import Faker
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random


class TestDataGenerator:
    def __init__(self):
        self.fake = Faker()

    def generate_name(self):
        return self.fake.name()

    def generate_password(self, length=10):
        return self.fake.password(length=length, special_chars=True, digits=True, upper_case=True, lower_case=True)

    def generate_word(self):
        return self.fake.word()

    def generate_amount(self):
        return self.fake.random_int(min=1, max=100)

    def generate_date(self):
        return f"{self.fake.date_time(): %d/%m/%Y}"

    @staticmethod
    def generate_future_date():
        future_date = datetime.now() + relativedelta(years=1)
        return f"{future_date: %d/%m/%Y}"

    @staticmethod
    def generate_string(size: int):
        return ''.join(random.choices(string.ascii_letters, k=size))
