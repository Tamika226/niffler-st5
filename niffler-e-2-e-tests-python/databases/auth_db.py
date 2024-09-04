from typing import Sequence

from sqlalchemy import create_engine, Engine
from sqlmodel import Session, select

from models.Auth import DbUser, DbAuthority


class AuthDb:

    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def get_all_users(self) -> Sequence[DbUser]:
        with Session(self.engine) as session:
            return session.exec(select(DbUser)).all()

    def get_user(self, user_name: str) -> DbUser | None:
        with Session(self.engine) as session:
            statement = select(DbUser).where(DbUser.username == user_name)
            return session.exec(statement).one()

    def update_enabled(self, username: str, enabled_value: bool):
        with Session(self.engine) as session:
            statement = select(DbUser).where(DbUser.username == username)
            user = session.exec(statement).one()
            user.enabled = enabled_value
            session.add(user)
            session.commit()
            session.refresh(user)

    def delete_user(self, username: str):
        user = self.get_user(username)
        with Session(self.engine) as session:
            statement = select(DbAuthority).where(DbAuthority.user_id == user.id)
            user_authorities = session.exec(statement).all
            session.delete(user_authorities)
            session.delete(user)
            session.commit()

    def delete_read_authority(self, username: str):
        user = self.get_user(username)
        with Session(self.engine) as session:
            statement = select(DbAuthority).where(DbAuthority.user_id == user.id and DbAuthority.authority == "read")
            user_authority = session.exec(statement).one
            session.delete(user_authority)
            session.commit()

    def delete_write_authority(self, username: str):
        user = self.get_user(username)
        with Session(self.engine) as session:
            statement = select(DbAuthority).where(DbAuthority.user_id == user.id and DbAuthority.authority == "write")
            user_authority = session.exec(statement).one
            session.delete(user_authority)
            session.commit()
