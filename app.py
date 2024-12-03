import streamlit as st
from citizen_page import citizen_interface
from authority_page import authority_interface

st.set_page_config(page_title="BBMP Citizen-Authority App", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Citizen Page", "Authority Page"])

if page == "Citizen Page":
    citizen_interface()
elif page == "Authority Page":
    authority_interface()
