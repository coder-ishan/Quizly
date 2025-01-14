import os
from google.cloud.sql.connector import Connector, IPTypes
import pg8000
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv



load_dotenv()

CLOUD_SQL_USERNAME = os.getenv('CLOUD_SQL_USERNAME')
CLOUD_SQL_PASSWORD = os.getenv('CLOUD_SQL_PASSWORD')
CLOUD_SQL_DATABASE_NAME = os.getenv('CLOUD_SQL_DATABASE_NAME')
CLOUD_SQL_CONNECTION_NAME = os.getenv('CLOUD_SQL_CONNECTION_NAME')


connector = Connector()


def getconn():
    conn = connector.connect(
        CLOUD_SQL_CONNECTION_NAME,
        "pg8000",
        user=CLOUD_SQL_USERNAME,
        password=CLOUD_SQL_PASSWORD,
        db=CLOUD_SQL_DATABASE_NAME,
    )
    return conn


engine = create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()