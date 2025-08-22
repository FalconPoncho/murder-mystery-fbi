from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker


DB_FILE = "mystery.db"
engine = create_engine(f"sqlite:///{DB_FILE}")

Base = declarative_base()
SessionLocal = sessionmaker(engine)


class Message(Base):
    id = Column(Integer, primary_key=True, index=True)
    