from urllib.parse import urljoin
from clients.base_client import BaseHttpClient
from models.Spend import NewSpend, Spend


class SpendsHttpClient(BaseHttpClient):
    def __init__(self, base_url: str, token: str):
        super().__init__(base_url, token)

    def add_spends(self, spend: NewSpend) -> Spend:
        url = urljoin(self.base_url, "/api/spends/add")
        response = self.session.post(url, json=spend.model_dump())
        response.raise_for_status()
        return Spend.model_validate(response.json())

    def remove_spends(self, ids: list[str]):
        url = urljoin(self.base_url, "/api/spends/remove")
        response = self.session.delete(url, params={"ids": ids})
        response.raise_for_status()

    def get_spends(self) -> list[Spend]:
        url = urljoin(self.base_url, "/api/spends/all")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
