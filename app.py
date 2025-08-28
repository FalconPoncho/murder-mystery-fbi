import streamlit as st
from db import init_db


init_db()

st.sidebar.image("static/images/fbi_logo_bw.png")

page_dict = {
    "home": st.Page("pages/home.py", title="Unified Access Portal"),
    "email": st.Page("pages/email.py", title="FBI Email"),
    "vars": st.Page("pages/vars.py", title="V.A.R.S."),
    "login": st.Page("pages/login.py", title="Unified Access Portal", default=True),
}

page_list = list(page_dict.values())

page = st.navigation(page_list, position="hidden")

st.sidebar.page_link(
    page_dict["home"],
    label="Home",
    icon=":material/house:",
    use_container_width=True,
)
st.sidebar.page_link(
    page_dict["email"],
    label="Email",
    icon=":material/mail:",
    use_container_width=True,
)
st.sidebar.page_link(
    page_dict["vars"],
    label="V.A.R.S.",
    icon=":material/visibility:",
    use_container_width=True,
)
st.sidebar.page_link(
    page_dict["login"],
    label="Sign out",
    icon=":material/logout:",
    use_container_width=True,
)

page.run()
