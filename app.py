import streamlit as st

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
