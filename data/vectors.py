import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Vector(SqlAlchemyBase):
    __tablename__ = 'VectorsId'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('UsersId.id'))
    vector = sqlalchemy.Column(sqlalchemy.Integer)

    user = orm.relation('User')
