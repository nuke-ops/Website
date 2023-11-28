import json

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

with open("config.json") as config:
    conf = json.loads(config.read())["sql"]

diceEngine = create_engine(
    f"mysql://{conf['user']}:{conf['password']}@{conf['host']}/{conf['database']}"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=diceEngine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
