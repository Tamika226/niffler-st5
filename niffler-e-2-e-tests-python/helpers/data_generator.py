from faker import Faker
from datetime import datetime, timedelta


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

    def future_date(self):
        future_date = datetime.now() + timedelta(days=self.one_period)
        return f"{future_date: %d/%m/%Y}"

