import streamlit as st


def check_authentication():
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.warning("Please log in to access this application")
        st.stop()
