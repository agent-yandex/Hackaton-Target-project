import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'UsersId'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    phone = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    vector = orm.relation('Vector', back_populates='user')
    product = orm.relation('Product', back_populates='user')
