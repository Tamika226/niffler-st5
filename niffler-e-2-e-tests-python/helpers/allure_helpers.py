import json
import logging
from json import JSONDecodeError

import allure
from playwright.sync_api import expect as original_expect
import curlify
from allure_commons.types import AttachmentType
from requests import Response


def allure_attach_request(function):
    """Декоратор логироваания запроса, хедеров запроса, хедеров ответа в allure шаг и аллюр аттачмент и в консоль."""
    def wrapper(*args, **kwargs):
        method, url = args[1], args[2]
        with allure.step(f"{method} {url}"):

            response: Response = function(*args, **kwargs)

            curl = curlify.to_curl(response.request)
            logging.debug(curl)
            logging.debug(response.text)

            allure.attach(
                body=curl.encode("utf8"),
                name=f"Request {response.status_code}",
                attachment_type=AttachmentType.TEXT,
                extension=".txt"
            )
            try:
                allure.attach(
                    body=json.dumps(response.json(), indent=4).encode("utf8"),
                    name=f"Response json {response.status_code}",
                    attachment_type=AttachmentType.JSON,
                    extension=".json"
                )
            except JSONDecodeError:
                allure.attach(
                    body=response.text.encode("utf8"),
                    name=f"Response text {response.status_code}",
                    attachment_type=AttachmentType.TEXT,
                    extension=".txt")
            allure.attach(
                body=json.dumps(dict(response.headers), indent=4).encode("utf8"),
                name=f"Response headers {response.status_code}",
                attachment_type=AttachmentType.JSON,
                extension=".json"
            )
        return response

    return wrapper


def attach_sql(statement, parameters, context):
    statement_with_params = statement % parameters
    name = statement.split(" ")[0] + " " + context.engine.url.database
    allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)

class LoggedExpect:
    def __init__(self, target):
        self.target = original_expect(target)

    def to_contain_text(self, text):
        with allure.step(f"Проверяем, что элемент содержит текст: '{text}'"):
            self.target.to_contain_text(text)

    def not_to_be_visible(self):
        with allure.step(f"Проверяем, что элемент не виден"):
            self.target.not_to_be_visible()

    def to_be_visible(self):
        with allure.step(f"Проверяем, что элемент виден"):
            self.target.to_be_visible()
