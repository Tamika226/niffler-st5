from typing import Sequence

from sqlalchemy import create_engine, Engine
from sqlmodel import Session, select

from models.Auth import User, Authority


class AuthDb:

    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def get_all_users(self) -> Sequence[User]:
        with Session(self.engine) as session:
            statement = select(User)
            return session.exec(statement).all()

    def get_user(self, user_name: str) -> User | None:
        with Session(self.engine) as session:
            statement = select(User).where(User.username == user_name)
            return session.exec(statement).first()

    def update_enabled(self, username: str, enabled_value: bool):
        with Session(self.engine) as session:
            statement = select(User).where(User.username == username)
            user = session.exec(statement).all()
            user.enabled = enabled_value
            session.add(user)
            session.commit()
            session.refresh(user)

    def delete_user(self, username: str):
        user = self.get_user(username)
        self.delete_read_authority(user)
        self.delete_write_authority(user)
        with Session(self.engine) as session:
            session.delete(user)
            session.commit()

    def delete_read_authority(self, user: User):
        with Session(self.engine) as session:
            statement = select(Authority).where(Authority.user_id == user.id and Authority.authority == "read")
            user_authority = session.exec(statement).first()
            session.delete(user_authority)
            session.commit()

    def delete_write_authority(self, user: User):
        with Session(self.engine) as session:
            statement = select(Authority).where(Authority.user_id == user.id and Authority.authority == "write")
            user_authority = session.exec(statement).first()
            session.delete(user_authority)
            session.commit()
