from sqlalchemy import Column, Integer, String, UUID
from database import Base
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable = True)
    user_name = Column(String, nullable = True, unique=True)
    email = Column(String, nullable = False, unique=True)
    phone_number = Column(String, nullable = True, unique=True)

