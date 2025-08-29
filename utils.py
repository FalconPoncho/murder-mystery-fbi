import streamlit as st
import pandas as pd
from db import engine, User, Message
from sqlalchemy import select, func
from sqlalchemy.orm import Session, aliased
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

def write_no_mailto(message: str, header_level: int = 0):
    safe_message = "@&#8203;".join(message.split("@"))
    if header_level:
        safe_message = "#"*header_level + " " + safe_message
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
        user_ = session.query(User).where(User.username == user).one()

        # Alias User for the aggregation join (so we can join to *all* recipients)
        Recip = aliased(User)

        # aggregate recipients into a CSV per message
        recipients_concat = func.group_concat(Recip.username, ', ').label("recipients_csv")

        # base select: message fields + aggregated recipients
        base_stmt = (
            select(
                Message.id,
                Message.sender_username,
                Message.subject,
                Message.body,
                Message.time,
                Message.attachment,
                recipients_concat,
            )
            .select_from(Message)
            .join(Recip, Message.recipients)   # join to all recipients for aggregation
            .group_by(Message.id)
            .order_by(Message.time.desc())
        )

        if relationship == "sender":
            # messages I sent (one row per message, recipients aggregated)
            stmt = base_stmt.where(Message.sender_username == user_.username)
        elif relationship == "recipient":
            # messages where I'm among recipients, but still aggregate *all* recipients
            stmt = base_stmt.where(Message.recipients.any(User.username == user_.username))
        else:
            stmt = base_stmt  # fallback / or raise

        mail = pd.read_sql(stmt, session.bind)

        users_ = users()  # your existing function returning users DataFrame

        # Merge sender details (same as before)
        mail = mail.merge(
            users_.rename(columns={"username": "sender_username"}),
            on="sender_username",
            how="left",
            suffixes=("", "_sender"),
        )

        # Convert CSV -> Python list for easier use in the app
        mail["recipient_usernames"] = mail["recipients_csv"].fillna("").apply(
            lambda s: [u.strip() for u in s.split(",")] if s else []
        )

        return mail

    # with Session(engine) as session:
    #     user_ = (
    #         session.query(User)
    #         .where(User.username == user)
    #         .one()
    #     )

    #     if relationship == "sender":
    #         query = (
    #             session.query(
    #                 Message.id,
    #                 Message.sender_username,
    #                 Message.subject,
    #                 Message.body,
    #                 Message.time,
    #                 User.username.label("recipient_username"),
    #             )
    #             .join(Message.recipients)  # bring in recipients
    #             .where(Message.sender_username == user_.username)
    #         )

    #     elif relationship == "recipient":
    #         query = (
    #             session.query(
    #                 Message.id,
    #                 Message.sender_username,
    #                 Message.subject,
    #                 Message.body,
    #                 Message.time,
    #                 User.username.label("recipient_username"),
    #             )
    #             .join(Message.recipients)  # bring in recipients
    #             .where(User.username == user_.username)
    #         )

    #     mail = pd.read_sql(query.statement, session.bind)

    #     users_ = users()

    #     # Merge sender details
    #     mail = mail.merge(
    #         users_.rename(columns={"username": "sender_username"}),
    #         on="sender_username",
    #         how="left",
    #         suffixes=("", "_sender"),
    #     )

    #     # Merge recipient details
    #     mail = mail.merge(
    #         users_.rename(columns={"username": "recipient_username"}),
    #         on="recipient_username",
    #         how="left",
    #         suffixes=("", "_recipient"),
    #     )

        return mail
        # query = session.query(Message)
        # if relationship == "sender":
        #     query = query.where(Message.sender_username.is_(user_.username))
        # elif relationship == "recipient":
        #     query.join(Message.recipients).where(User.username == user_.username)
        #     # query = query.where(Message.recipient_username.is_(user_.username))

        # mail = pd.read_sql(
        #     query.statement,
        #     session.bind
        # )

        # users_ = users()

        # mail = mail.merge(
        #     users_.rename(columns={"username": "sender_username"}),
        #     on="sender_username",
        #     how="left",
        # )
        # mail = mail.merge(
        #     users_.rename(columns={"username": "recipient_username"}),
        #     on="recipient_username",
        #     how="left",
        # )

        # return mail

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
