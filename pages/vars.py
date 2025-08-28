import streamlit as st


INSTRUCTIONS = """
V.A.R.S. is the authorized interface for accessing I.R.I.S. (Integrated Retinal Imaging & Surveillance) recordings. Access codes are issued conditional on search warrants.

For help filing a US Courts AO 93 Search and Seizure Warrant, contact your OGC representative.
"""

TERMS_OF_USE = """
I.R.I.S. Footage Access Disclaimer

The Visual Archive Retrieval System (V.A.R.S.) provides controlled access to I.R.I.S. (Integrated Retinal Imaging & Surveillance) video recorded from authorized Neuralink implants. Access to I.R.I.S. content is restricted to specific investigative needs and is governed by Fourth Amendment protections against unreasonable searches and seizures, along with applicable statutes and agency policy.

By submitting a request, you affirm that:

- You are seeking narrowly tailored footage tied to a legitimate investigative purpose.
- Your request identifies a specific agent, date, and precise time window.
- You understand that no bulk, continuous, or exploratory retrieval is permitted.

All requests are subject to judicial review. A search warrant may be issued conditional on probable cause supported by a clear justification.

If approved, V.A.R.S. will issue a single-use Access Code which can be obtained from the judicial authority. Entering that code will decrypt only the footage authorized in the search warrant. All access events are logged and auditable. Unauthorized use or sharing of codes is prohibited and subject to administrative and criminal penalties.
"""

INVALID = """
Invalid access code.

All usage of V.A.R.S. is monitored and logged. Unauthorized use of V.A.R.S. is subject to administrative and criminal penalties.
"""


st.set_page_config(layout="centered")

videos = {"test": "static/videos/MurderFootage.mp4"}

st.title("Visual Archive Retrieval System")

st.text(INSTRUCTIONS)

st.header("Terms of Use")
with st.container(height=200):
    st.text(TERMS_OF_USE)
accepted_tos = st.checkbox("I have read and accept the terms of use.")

if accepted_tos:
    with st.form("vars"):
        code = st.text_input(
            "Access Code",
            placeholder="Enter access code"
        )
        submitted = st.form_submit_button()
        if submitted:
            if code in videos:
                st.video(videos[code])
            else:
                st.error(INVALID)