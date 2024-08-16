import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

#
SQLALCHEMY_DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URL')
print("Database opened for connection")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
print("Database connecting.....................")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = sqlalchemy.orm.declarative_base()

print("Database connection established")
# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
