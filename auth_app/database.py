from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config_parser import config

SQLALCHEMY_DATABASE_URL = f"postgresql://{config()['POSTGRES']['user']}:" \
                          f"{config()['POSTGRES']['password']}@{config()['POSTGRES']['host']}:" \
                          f"{config()['POSTGRES']['port']}/{config()['POSTGRES']['db_name']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
