from pydantic import BaseModel


class Envs(BaseModel):
    app_url: str
    auth_url: str
    gateway_url: str
    default_timeout: int
    default_user_login: str
    default_user_password: str
