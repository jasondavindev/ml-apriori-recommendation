from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from os import getenv
from dotenv import load_dotenv

load_dotenv()


DB_ENDPOINT = getenv("DB_ENDPOINT")
DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")
DB_NAME = getenv("DB_NAME")

engine_str = (
    "mysql+pymysql://"
    + DB_USER
    + ":"
    + DB_PASS
    + "@"
    + DB_ENDPOINT
    + "/"
    + DB_NAME
    + "?charset=latin1"
)

Engine = create_engine(engine_str)

Base = declarative_base()

Session = sessionmaker(Engine)
session = Session()
