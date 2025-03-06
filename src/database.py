from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import Annotated
from fastapi import Depends
from gobal_variables import DB_URI, REDIS_HOST, REDIS_PORT
from sqlalchemy import Column, DateTime, func
from contextlib import asynccontextmanager
import redis.asyncio as redis
from fastapi import FastAPI


# global redis connector
redis_client = None

# postgres database url
postgres_url = DB_URI

# create engine for database connection
engine = create_engine(postgres_url)

# creating session for orms
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)


# base class initiated
class Base(DeclarativeBase):
    __abstract__ = True

    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, default = func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)


# redis setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
        setting up redis server on will start on startup
    '''

    global redis_client
    print("Starting redis server on startup...")
    redis_client = await redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    yield

    print("Shutting down redis server on shutdown...")
    redis_client.close()




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
