import sqlalchemy
from loader import Base


class Link(Base):
    __tablename__ = "links"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    crm_user_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    text = sqlalchemy.Column(sqlalchemy.VARCHAR(200), nullable=True, default='У вас нет ссылки на занятие')
