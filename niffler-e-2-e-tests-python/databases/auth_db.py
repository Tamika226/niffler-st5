from typing import Sequence

import allure
from allure_commons.types import AttachmentType
from sqlalchemy import create_engine, event
from sqlmodel import Session, select

from models.Auth import User, Authority


class AuthDb:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        event.listen(self.engine, "do_execute", fn=self.attach_sql)

    @staticmethod
    def attach_sql(cursor, statement, parameters, context):
        statement_with_params = statement % parameters
        name = statement.split(" ")[0] + " " + context.engine.url.database
        allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)

    @allure.step("Получаем всех пользователей из БД")
    def get_all_users(self) -> Sequence[User]:
        with Session(self.engine) as session:
            statement = select(User)
            return session.exec(statement).all()

    def get_user(self, username: str) -> User | None:
        with (allure.step(f"Получаем пользователя из БД с username = {username}")):
            with Session(self.engine) as session:
                statement = select(User).where(User.username == username)
                return session.exec(statement).first()

    def update_enabled(self, username: str, enabled_value: bool):
        with (allure.step(f"Для пользователя username = {username} устанавливаем значение enabled_value = {enabled_value} ")):
            with Session(self.engine) as session:
                statement = select(User).where(User.username == username)
                user = session.exec(statement).all()
                user.enabled = enabled_value
                session.add(user)
                session.commit()
                session.refresh(user)

    def delete_user(self, username: str):
        with (allure.step(f"Удаляем пользователя из БД с username = {username}")):
            user = self.get_user(username)
            self.delete_read_authority(user)
            self.delete_write_authority(user)
            with Session(self.engine) as session:
                session.delete(user)
                session.commit()

    def delete_read_authority(self, user: User):
        with (allure.step(f"Удаляем для пользователя из БД с username = {user.username} права на чтение")):
            with Session(self.engine) as session:
                statement = select(Authority).where(Authority.user_id == user.id and Authority.authority == "read")
                user_authority = session.exec(statement).first()
                session.delete(user_authority)
                session.commit()


    def delete_write_authority(self, user: User):
        with (allure.step(f"Удаляем для пользователя из БД с username = {user.username} права на запись")):
            with Session(self.engine) as session:
                statement = select(Authority).where(Authority.user_id == user.id and Authority.authority == "write")
                user_authority = session.exec(statement).first()
                session.delete(user_authority)
                session.commit()

