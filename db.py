import streamlit as st
from sqlalchemy import create_engine, Column, Integer, Text, DateTime, ForeignKey, Boolean, Table
from sqlalchemy.orm import declarative_base, Session, relationship
from datetime import datetime
import json
import os


DB_FILE = "mystery.db"
engine = create_engine(f"sqlite:///{DB_FILE}")

Base = declarative_base()


message_recipients = Table(
    "message_recipients",
    Base.metadata,
    Column("message_id", Integer, ForeignKey("messages.id"), primary_key=True),
    Column("recipient_username", Text, ForeignKey("users.username"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    username = Column(Text, primary_key=True)
    password = Column(Text)
    real = Column(Boolean, nullable=False)

    sent_messages = relationship(
        "Message",
        back_populates="sender",
        foreign_keys="[Message.sender_username]"
    )

    received_messages = relationship(
        "Message",
        secondary=message_recipients,
        back_populates="recipients"
    )

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_username = Column(Text, ForeignKey("users.username"), nullable=False)
    subject = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    time = Column(DateTime, nullable=False)

    sender = relationship(
        "User",
        back_populates="sent_messages",
        foreign_keys=[sender_username]
    )

    recipients = relationship(
        "User",
        secondary=message_recipients,
        back_populates="received_messages"
    )

# class User(Base):
#     __tablename__ = "users"

#     username = Column(Text, primary_key=True)
#     password = Column(Text)
#     real = Column(Boolean, nullable=False)

#     sent_messages = relationship("Message", back_populates="sender", foreign_keys="[Message.sender_username]")
#     received_messages = relationship("Message", back_populates="recipient", foreign_keys="[Message.recipient_username]")


# class Message(Base):
#     __tablename__ = "messages"
#     id = Column(Integer, primary_key=True, index=True)
#     sender_username = Column(Integer, ForeignKey("users.username"), nullable=False)
#     recipient_username = Column(Integer, ForeignKey("users.username"), nullable=False)
#     recipients = Column()
#     subject = Column(Text, nullable=False)
#     body = Column(Text, nullable=False)
#     time = Column(DateTime, nullable=False)

#     sender = relationship("User", back_populates="sent_messages", foreign_keys=[sender_username])
#     recipient = relationship("User", back_populates="received_messages", foreign_keys=[recipient_username])


@st.cache_data
def init_db():
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        if session.query(User).count() == 0:
            users = [
                User(username="amanda.j.garcia@fbi.gov", password="$$qu33nb33$$", real=True),
                User(username="marcus.d.holloway@fbi.gov", password="BureauLawyer39#(", real=True),
                User(username="wyatt.e.turk@fbi.gov", password="$1337techbro$", real=True),
                User(username="noah.f.englund@fbi.gov", password="usa1USA!", real=True),
                User(username="amelia.p.goulding@fbi.gov", password="xXl1v3_f4stXx", real=True),
                User(username="rachel.m.moore@fbi.gov", password="r10d3j4n31r0!", real=True),
                User(username="oliver.h.cox@fbi.gov", password="freudwasright1!", real=True),
                User(username="nick.k.anand@fbi.gov", password="amanda<3", real=True),
                User(username="maverick.w.bell@fbi.gov", password="@ssk1cker", real=True),
                User(username="ava.y.violet@fbi.gov", password="f0xyl@dy", real=True),
                
            ]
            session.add_all(users)
            session.commit()

        if session.query(Message).count() == 0:
            users_by_email = {u.username: u for u in session.query(User).all()}

            for filepath in os.listdir("mail"):
                with open(os.path.join("mail", filepath), "r") as file:
                    file_contents = json.load(file)

                messages = []
                for email in file_contents:
                    # look up sender
                    print(email)
                    sender = session.query(User).filter_by(username=email["sender_username"]).one()

                    # look up recipients (list of User objects)
                    recipient_users = (
                        session.query(User)
                        .filter(User.username.in_(email["recipients"]))
                        .all()
                    )

                    msg = Message(
                        sender=sender,
                        recipients=recipient_users,
                        subject=email["subject"],
                        body=email["body"],
                        time=datetime.fromisoformat(email["time"]),
                    )
                    messages.append(msg)

                session.add_all(messages)

            # sample_messages = [
            #     Message(sender_username="amanda.garcia@fbi.gov", recipients=[users_by_email["marcus.holloway@fbi.gov"], users_by_email["amanda.garcia@fbi.gov"]],
            #             subject="Hello Marcus!", body="Just wanted to say hi.", time=datetime(2070, 8, 1, 12, 30)),
            #     Message(sender_username="marcus.holloway@fbi.gov", recipients=[users_by_email["amanda.garcia@fbi.gov"]],
            #             subject="Meeting Update", body="Meeting moved to 3 PM.", time=datetime(2070, 8, 1, 14, 45)),
            # ]
            # session.add_all(sample_messages)

            session.commit()
        print("Added data to database")