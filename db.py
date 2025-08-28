import streamlit as st
from sqlalchemy import create_engine, Column, Integer, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, Session, relationship
from datetime import datetime
import json
import os


DB_FILE = "mystery.db"
engine = create_engine(f"sqlite:///{DB_FILE}")

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    username = Column(Text, primary_key=True)
    password = Column(Text)
    real = Column(Boolean, nullable=False)

    sent_messages = relationship("Message", back_populates="sender", foreign_keys="[Message.sender_username]")
    received_messages = relationship("Message", back_populates="recipient", foreign_keys="[Message.recipient_username]")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_username = Column(Integer, ForeignKey("users.username"), nullable=False)
    recipient_username = Column(Integer, ForeignKey("users.username"), nullable=False)
    subject = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    time = Column(DateTime, nullable=False)

    sender = relationship("User", back_populates="sent_messages", foreign_keys=[sender_username])
    recipient = relationship("User", back_populates="received_messages", foreign_keys=[recipient_username])


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

            for filepath in os.listdir("mail"):
                with open(os.path.join("mail", filepath), "r") as file:
                    file_contents = json.load(file)
                
                messages = [
                    Message(
                        sender_username=email["sender_username"],
                        recipient_username=email["recipient_username"],
                        subject=email["subject"],
                        body=email["body"],
                        time=datetime.fromisoformat(email["time"])
                    )
                    for email in file_contents
                ]
                session.add_all(messages)
            sample_messages = [
                Message(sender_username="amanda.garcia@fbi.gov", recipient_username="marcus.holloway@fbi.gov",
                        subject="Hello Marcus!", body="Just wanted to say hi.", time=datetime(2070, 8, 1, 12, 30)),
                Message(sender_username="marcus.holloway@fbi.gov", recipient_username="amanda.garcia@fbi.gov",
                        subject="Meeting Update", body="Meeting moved to 3 PM.", time=datetime(2070, 8, 1, 14, 45)),
            ]
            session.add_all(sample_messages)
            session.commit()
        print("Added data to database")