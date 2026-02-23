# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import   mapper_registry

DB_PATH = "labellobster.db"

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)

# Tabellen erzeugen, falls DB neu ist
mapper_registry.metadata.create_all(engine)

def get_session():
    return SessionLocal()

