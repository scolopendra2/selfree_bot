import sqlalchemy

from loader import Base


class Message(Base):
    __tablename__ = "messages"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tg_user_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    text = sqlalchemy.Column(sqlalchemy.VARCHAR(200), nullable=True, default='Пользователь не отправил текст')
    photo = sqlalchemy.Column(sqlalchemy.VARCHAR(200), nullable=True, default='Нет фото')