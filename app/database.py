from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:#D1234G#@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionnLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

# Setting up function to get the DB
def get_db():
    db = SessionnLocal()
    try:
        yield db
    finally:
        db.close()