import sqlalchemy
from loader import Base


class Homework(Base):
    __tablename__ = "homeworks"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    crm_user_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    text = sqlalchemy.Column(sqlalchemy.VARCHAR(200), nullable=True, default='У вас нет домашнего задания')
    photo = sqlalchemy.Column(sqlalchemy.VARCHAR(200), nullable=True, default='У вас нет домашнего задания')
