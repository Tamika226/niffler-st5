from faker import Faker


class TestDataGenerator:
    def __init__(self):
        self.fake = Faker()

    def generate_name(self):
        return self.fake.name()

    def generate_password(self, length=10):
        return self.fake.password(length=length, special_chars=True, digits=True, upper_case=True, lower_case=True)

    def generate_word(self):
        return self.fake.word()

