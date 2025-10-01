# streamlit_app.py
import streamlit as st
from agenticcv import cvmaster

st.set_page_config(page_title="Agentic CV Generator", layout="centered")
st.title("Agentic CV Generator")

with st.form("cv_form"):
    name = st.text_input("Full Name")
    contact_number = st.text_input("Contact Number")
    email = st.text_input("Email Address")
    github = st.text_input("GitHub Username")
    linkedin = st.text_input("LinkedIn Username")
    summary = st.text_area("Professional Summary")
    # Add repeatable AJAX-like st.experimental_data_editor for Education, Skills, etc.
    submitted = st.form_submit_button("Generate Resume")

if submitted:
    # Interface with your existing class
    cv = cvmaster()
    data = (contact_number, email, github, linkedin)
    # Optionally, set environment variables or API keys
    # Compose the rest of the sections as per your method signatures
    # Call methods from the original code to generate each section
    result = cv.finalize()  # Adapt parameters as needed
    st.markdown(result, unsafe_allow_html=True)
    # Optionally add download button for HTML/PDF if supported
