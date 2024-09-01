from pydantic import BaseModel,Field


class NewSpend(BaseModel):
    amount: float
    category: str
    currency: str
    description: str
    spendDate: str


class Spend(NewSpend):
    id: str
    username: str
