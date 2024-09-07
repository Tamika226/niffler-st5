import re


class StringHelper:

    @staticmethod
    def camel_to_sentence(camel_str):
        sentence = re.sub(r'(?<!^)(?=[A-Z])', ' ', camel_str)
        return sentence.capitalize()