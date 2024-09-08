import allure
from allure_commons.types import AttachmentType
from typing import Sequence

from sqlalchemy import create_engine, event
from sqlmodel import Session, select

from models.Spend import Category, Spend


class SpendDb:

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        event.listen(self.engine, "do_execute", fn=self.attach_sql)

    @staticmethod
    def attach_sql(cursor, statement, parameters, context):
        statement_with_params = statement % parameters
        name = statement.split(" ")[0] + " " + context.engine.url.database
        allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)


    def get_user_categories(self, username: str) -> Sequence[Category]:
        with (allure.step(f"Получаем все категории пользователя username = {username}")):
            with Session(self.engine) as session:
                statement = select(Category).where(Category.username == username)
                return session.exec(statement).all()


    def delete_category(self, category_id: str):
        with (allure.step(f"Удаляем категорию category_id = {category_id}")):
            with Session(self.engine) as session:
                category = session.get(Category, category_id)
                session.delete(category)
                session.commit()

    def get_spend(self, spend_id: str) -> Spend:
        with (allure.step(f"Получаем трату по spend_id = {spend_id}")):
            with Session(self.engine) as session:
                statement = select(Spend).where(Spend.id == spend_id)
                return session.exec(statement).one()
