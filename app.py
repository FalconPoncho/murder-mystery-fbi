import streamlit as st
from sqlalchemy import text
from backend.login import login

FOUO_WARNING = """
Use of this system is \"FOR OFFICIAL USE ONLY\". \
This system is subject to monitoring. Therefore, \
no expectation of privacy is to be assumed. \
Individuals found performing unauthorized activities \
may be subject to disciplinary action including \
criminal prosecution. \
"""

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
                st.switch_page("pages/Home.py")

def homepage():
    hide_sidebar()

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

homepage()

# # Create the SQL connection to pets_db as specified in your secrets file.
# conn = st.connection('pets_db', type='sql')

# # Insert some data with conn.session.
# with conn.session as s:
#     s.execute(text('CREATE TABLE IF NOT EXISTS pet_owners (person TEXT, pet TEXT);'))
#     s.execute(text('DELETE FROM pet_owners;'))
#     pet_owners = {'jerry': 'fish', 'barbara': 'cat', 'alex': 'puppy'}
#     for k in pet_owners:
#         s.execute(
#             text('INSERT INTO pet_owners (person, pet) VALUES (:owner, :pet);'),
#             params=dict(owner=k, pet=pet_owners[k])
#         )
#     s.commit()

# # Query and display the data you inserted
# pet_owners = conn.query('select * from pet_owners')
# st.dataframe(pet_owners)