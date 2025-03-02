from database import Base
from sqlalchemy import Column, DateTime, func

class CommonModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, func.now())
    updated_at = Column(DateTime, func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)