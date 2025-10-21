from clients.base_client import BaseHttpClient
from models.Spend import NewSpend, Spend


class SpendsHttpClient(BaseHttpClient):
    def __init__(self, base_url: str, token: str):
        super().__init__(base_url, token)

    def add_spends(self, spend: NewSpend) -> Spend:
        response = self.session.post("/api/spends/add", json=spend.model_dump())
        response.raise_for_status()
        return Spend.model_validate(response.json())

    def remove_spends(self, ids: list[str]):
        response = self.session.delete("/api/spends/remove", params={"ids": ids})
        response.raise_for_status()

    def get_spends(self) -> list[Spend]:
        response = self.session.get("/api/spends/all")
        response.raise_for_status()
        return response.json()
