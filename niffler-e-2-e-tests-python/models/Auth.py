from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class PreRequest(BaseModel):
    response_type: str
    scope: str
    client_id: str
    redirect_uri: str
    code_challenge: str
    code_challenge_method: str


class Login(BaseModel):
    username: str
    password: str
    _csrf: str


class Token(BaseModel):
    code: str | None
    redirect_uri: str
    code_verifier: str
    grant_type: str
    client_id: str


class TokenResponse(BaseModel):
    access_token: str
    scope: str
    id_token: str
    token_type: str
    expires_in: int
    refresh_token: str | None = None


class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    username: str
    password: str
    enabled: bool
    account_non_expired: bool
    account_non_locked: bool
    credentials_non_expired: bool


class Authority(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str
    authority: str
