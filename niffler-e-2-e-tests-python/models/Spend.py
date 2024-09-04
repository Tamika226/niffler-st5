from sqlmodel import SQLModel, Field


class NewSpend(SQLModel):
    amount: float
    category: str
    currency: str
    description: str
    spendDate: str


class Spend(NewSpend):
    id: str = Field(default=None, primary_key=True)
    username: str


class Category(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    category: str
    username: str
