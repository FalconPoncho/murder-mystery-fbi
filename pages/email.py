import streamlit as st
import pandas as pd


def open_mail():
    index = st.session_state.selected_mail["selection"]["rows"][0]
    st.session_state.open_mail = st.session_state.all_mail.iloc[index]


st.set_page_config(layout="wide")

columns = st.columns([1,5])

with columns[0]:
    selected_mailbox = "Inbox"
    def select_mailbox(value):
        selected_mailbox = value
        st.session_state.open_mail = None
    for option in ("Inbox", "Sent", "Drafts"):
        st.button(
            option,
            type="primary",
            use_container_width=True,
            on_click=select_mailbox,
            args=[option],
        )

with columns[1]:
    if st.session_state.open_mail is None:
        st.session_state.all_mail = pd.DataFrame({
            "id": [6,7,8,9],
            "From": [1,2,3,4],
            "Title": [5,6,7,8],
        })
        selection = st.dataframe(
            st.session_state.all_mail,
            column_order=("From", "Title"),
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
        st.write("This is an email.")
