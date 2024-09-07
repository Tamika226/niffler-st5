from urllib.parse import urljoin
from clients.base_client import BaseHttpClient
import requests


class SpendsHttpClient(BaseHttpClient):
    def __init__(self, base_url: str, token: str):
        super().__init__(base_url, token)

    def add_spends(self, body):
        url = urljoin(self.base_url, "/api/spends/add")
        response = self.session.post(url, json=body)
        response.raise_for_status()
        return response.json()

    def remove_spends(self, ids: list[int]):
        url = urljoin(self.base_url, "/api/spends/remove")
        response = self.session.delete(url, params={"ids": ids})
        response.raise_for_status()

    def get_spends(self):
        url = urljoin(self.base_url, "/api/spends/all")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()