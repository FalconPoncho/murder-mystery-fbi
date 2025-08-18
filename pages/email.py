import streamlit as st
import pandas as pd


st.set_page_config(layout="wide")

columns = st.columns([1,5])

with columns[0]:
    selected_mailbox = "Inbox"
    def select_mailbox(value):
        selected_mailbox = value
    for option in ("Inbox", "Sent", "Drafts"):
        st.button(
            option,
            type="primary",
            use_container_width=True,
            on_click=select_mailbox,
            args=[option],
        )

with columns[1]:
    mail = pd.DataFrame({
        "col1": [1,2,3,4],
        "col2": [5,6,7,8],
    })
    st.dataframe(mail)