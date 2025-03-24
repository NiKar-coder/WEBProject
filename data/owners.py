import sqlalchemy
from .db_session import SqlAlchemyBase


class Owner(SqlAlchemyBase):
    __tablename__ = 'owners'

    number = sqlalchemy.Column(sqlalchemy.Integer,
                               primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    patronymic = sqlalchemy.Column(sqlalchemy.String)
    flat = sqlalchemy.Column(sqlalchemy.String)
    phone = sqlalchemy.Column(sqlalchemy.String)
    carsModel = sqlalchemy.Column(sqlalchemy.String)
