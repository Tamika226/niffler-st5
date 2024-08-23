from urllib.parse import urljoin
from clients.base_client import BaseHttpClient
import requests


class CategoriesHttpClient(BaseHttpClient):
    def __init__(self, base_url: str, token: str):
        super().__init__(base_url, token)

    def get_categories(self):
        response = self.session.get(urljoin(self.base_url, "/api/categories/all"))
        response.raise_for_status()
        return response.json()

    def add_category(self, name: str):
        response = self.session.post(urljoin(self.base_url, "/api/categories/add"), json={
            "category": name
        })
        response.raise_for_status()
        return response.json()
