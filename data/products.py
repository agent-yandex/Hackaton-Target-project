import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'ProdectsId'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('UsersId.id'))
    json_file = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    user = orm.relation('User')
