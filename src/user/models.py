from sqlalchemy import Column, Integer, String, Boolean, UUID, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable = True)
    user_name = Column(String, nullable = True, unique=True)
    email = Column(String, nullable = False, unique=True)
    phone_number = Column(String, nullable = True, unique=True)

    # relations
    users_connection = relationship("users_connection", back_populates="users")

class UserConnections(Base):
    __tablename__ = "users_connection"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    user_connection_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    user_connection_name = Column(String, nullable = False, unique = True)
    is_muted = Column(Boolean, default=False, nullable=False)

    # relations
    user = relationship("users", back_populates="users_connection")



