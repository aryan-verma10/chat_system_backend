from sqlalchemy import Column, Integer, String
from src.utilities import CommonModel


class User(CommonModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable = True)
    user_name = Column(String, nullable = False, unique=True)
    email = Column(String, nullabe = False, unique=True)
    phone_number = Column(String, nullable = True, unique=True)

