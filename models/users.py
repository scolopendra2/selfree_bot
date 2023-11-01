import sqlalchemy
from loader import Base


class User(Base):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.VARCHAR(200))
    tg_user_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    crm_user_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    phone = sqlalchemy.Column(sqlalchemy.VARCHAR(200))
    is_student = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=True)