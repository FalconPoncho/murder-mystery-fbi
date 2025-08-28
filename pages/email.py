import streamlit as st
import pandas as pd
from utils import write_no_mailto, mail


def open_mail():
    index = st.session_state.selected_mail["selection"]["rows"][0]
    st.session_state.open_mail = st.session_state.all_mail.iloc[index]


st.set_page_config(layout="wide")

columns = st.columns([1,5])

with columns[0]:
    if "selected_mailbox" not in st.session_state:
        st.session_state.selected_mailbox = "Inbox"
    def select_mailbox(value):
        st.session_state.selected_mailbox = value
        st.session_state.open_mail = None
    for option in ("Inbox", "Sent"):#, "Drafts"):
        st.button(
            option,
            type="primary",
            use_container_width=True,
            on_click=select_mailbox,
            args=[option],
        )

with columns[1]:
    if st.session_state.open_mail is None:
        # st.session_state.all_mail = pd.DataFrame({
        #     "id": [6,7,8,9],
        #     "From": [1,2,3,4],
        #     "Title": [5,6,7,8],
        # })
        if st.session_state.selected_mailbox == "Inbox":
            relationship = "recipient"
        elif st.session_state.selected_mailbox == "Sent":
            relationship = "sender"

        st.session_state.all_mail = mail(st.session_state.username, relationship)

        selection = st.dataframe(
            st.session_state.all_mail.loc[:, ["sender_username", "subject", "time"]],
            column_order=("sender_username", "subject", "time"),
            # column_config={
            #     "id": st.column_config.Column(),
            #     "Title": st.column_config.TextColumn(width=100),
            #     "Text": st.column_config.TextColumn(),
            # },
            on_select=open_mail,
            selection_mode="single-row",
            key="selected_mail",
            hide_index=True,
        )
    else:
        header = st.columns([2,1])
        with header[0]:
            write_no_mailto(st.session_state.open_mail["sender_username"], header_level=3)
            write_no_mailto(f"to {st.session_state.open_mail['recipient_username']}")
        with header[1]:
            time = st.session_state.open_mail["time"].strftime("%A, %d %b %Y %H:%M")
            st.markdown(f'<div style="text-align: right;">{time}</div>', unsafe_allow_html=True)
        st.header(st.session_state.open_mail["subject"])
        st.write(st.session_state.open_mail["body"])
