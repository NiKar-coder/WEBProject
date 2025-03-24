import sqlalchemy
from .db_session import SqlAlchemyBase


class Owner(SqlAlchemyBase):
    __tablename__ = 'owners'

    carsNumber = sqlalchemy.Column(sqlalchemy.String,
                                   primary_key=True)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    patronymic = sqlalchemy.Column(sqlalchemy.String)
    flat = sqlalchemy.Column(sqlalchemy.String)
    phone = sqlalchemy.Column(sqlalchemy.String)
    carsModel = sqlalchemy.Column(sqlalchemy.String)
