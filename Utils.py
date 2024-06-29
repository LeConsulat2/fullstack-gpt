# utils.py
import streamlit as st


def check_authentication():
    if not st.session_state.get("authenticated", False):
        st.warning("Please log in to access this application")
        st.info("Please click 'Home' on the left sidebar to log in.")
        st.stop()
