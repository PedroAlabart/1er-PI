# database_connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from config import DATABASE_URL


# Engine singleton (echo=True es útil solo en dev)
engine = create_engine(DATABASE_URL, echo=False)

# Creador de sesiones moderno
SessionLocal = sessionmaker(bind=engine, class_=Session)

# Funciones utilitarias
def get_engine():
    return engine

def get_session() -> Session:
    return SessionLocal()