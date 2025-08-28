import streamlit as st
from sqlalchemy import create_engine, Column, Integer, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, Session, relationship
from datetime import datetime


DB_FILE = "mystery.db"
engine = create_engine(f"sqlite:///{DB_FILE}")

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, unique=True, nullable=False)
    password = Column(Text)
    real = Column(Boolean, nullable=False)

    sent_messages = relationship("Message", back_populates="sender", foreign_keys="[Message.sender_id]")
    received_messages = relationship("Message", back_populates="recipient", foreign_keys="[Message.recipient_id]")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    time = Column(DateTime, nullable=False)

    sender = relationship("User", back_populates="sent_messages", foreign_keys=[sender_id])
    recipient = relationship("User", back_populates="received_messages", foreign_keys=[recipient_id])


@st.cache_data
def init_db():
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        if session.query(User).count() == 0:
            users = [
                User(username="amanda.garcia@fbi.gov", password="test", real=True),
                User(username="marcus.holloway@fbi.gov", password="test", real=True),
            ]
            session.add_all(users)
            session.commit()

        if session.query(Message).count() == 0:
            users_by_email = {u.username: u for u in session.query(User).all()}

            sample_messages = [
                Message(sender=users_by_email["amanda.garcia@fbi.gov"], recipient=users_by_email["marcus.holloway@fbi.gov"],
                        subject="Hello Marcus!", body="Just wanted to say hi.", time=datetime(2070, 8, 1, 12, 30)),
                Message(sender=users_by_email["marcus.holloway@fbi.gov"], recipient=users_by_email["amanda.garcia@fbi.gov"],
                        subject="Meeting Update", body="Meeting moved to 3 PM.", time=datetime(2070, 8, 1, 14, 45)),
            ]
            session.add_all(sample_messages)
            session.commit()
        print("Added data to database")