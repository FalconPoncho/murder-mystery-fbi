import streamlit as st
from sqlalchemy import text
from backend.login import login
from utils.utils import hide_sidebar


FOUO_WARNING = """
Use of this system is \"FOR OFFICIAL USE ONLY\". \
This system is subject to monitoring. Therefore, \
no expectation of privacy is to be assumed. \
Individuals found performing unauthorized activities \
may be subject to disciplinary action including \
criminal prosecution. \
"""

def login_box():
    """
    Provide a box for username and password entry.

    """
    with st.form("login", border=True):
        username = st.text_input(
            "Username",
            placeholder="Enter username",
        )
        password = st.text_input(
            "Password",
            placeholder="Enter password",
            type="password"
        )
        submitted = st.form_submit_button(label="Login", width="stretch")
        st.markdown("Forgot your password? **Think harder.**")

        if submitted:
            success = login(username=username, password=password)
            if success:
                st.session_state["username"] = username
                st.switch_page("pages/home.py")


st.set_page_config(layout="centered")

hide_sidebar()

st.session_state.open_mail = None

image_cols = st.columns(3)
image_cols[1].image("static/images/fbi_logo_bw.png")

columns = st.columns([1,6,1])
with columns[1]:
    title = "Unified Access Portal"
    st.markdown(
        f"""
        <h1 style='text-align: center; font-size: 45px;'>{title}</h1>
        """,
        unsafe_allow_html=True,
    )
    login_box()

st.text(FOUO_WARNING)
