import streamlit as st
import pandas as pd
from db import engine, User, Message
from sqlalchemy.orm import Session
from typing import Literal

def hide_sidebar():
    """
    Hide the sidebar using html injection.

    """
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] { display: none !important; }
            [data-testid="collapsedControl"] { display: none !important; }
        </style>
    """,
        unsafe_allow_html=True,
    )

def write_no_mailto(message: str):
    safe_message = "@&#8203;".join(message.split("@"))
    st.markdown(safe_message, unsafe_allow_html=True)

@st.cache_data
def users() -> pd.DataFrame:
    with Session(engine) as session:
        users = pd.read_sql(
            session.query(User).statement,
            session.bind
        )
    return users


@st.cache_data
def mail(
        user: str,
        relationship: Literal["sender", "recipient"] | None = None
    ) -> pd.DataFrame:
    """
    Get a pd.DataFrame of all of a given user's mail.

    Parameters
    ----------
    user : str
        Username.
    relationship : "sender", "recipient", or None, default None
        Whether to get only mail sent, only mail received, or all mail.

    """
    with Session(engine) as session:
        user_ = (
            session.query(User)
            .where(User.username == user)
            .one()
        )

        query = session.query(Message)
        if relationship == "sender":
            query = query.where(Message.sender_username.is_(user_.username))
        elif relationship == "recipient":
            query = query.where(Message.recipient_username.is_(user_.username))

        mail = pd.read_sql(
            query.statement,
            session.bind
        )

        users_ = users()

        mail = mail.merge(
            users_.rename(columns={"username": "sender_username"}),
            on="sender_username",
            how="left",
        )
        mail = mail.merge(
            users_.rename(columns={"username": "recipient_username"}),
            on="recipient_username",
            how="left",
        )

        return mail

def login(username: str, password: str):
    users_ = users()
    user_row = users_.loc[users_["username"] == username]
    if user_row.empty:
        st.error("User does not exist")
        return False
    if user_row.iloc[0]["password"] == password:
        return True
    else:
        st.error("Incorrect password")
        return False
