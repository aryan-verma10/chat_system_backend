from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import Annotated
from fastapi import Depends
from .gobal_variables import DB_URI


print("DCCC->", DB_URI)
# postgres database url
postgres_url = DB_URI

# create engine for database connection
engine = create_engine(postgres_url)

# creating session for orms
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)


# base class initiated
class Base(DeclarativeBase):
    pass


def get_session():
    '''
        function to provide session of orm of api endpoints
    '''
    db = session()
    try:
        yield db

    finally:
        db.close()


# Session is annotated to be used in apis later directly
session_dep = Annotated[Session, Depends(get_session)]
