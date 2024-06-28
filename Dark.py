# config.py

import streamlit as st


def set_page_config(page_title, page_icon):
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="centered",
        initial_sidebar_state="auto",
    )
    # Set the theme to dark mode
    st.write(
        """
        <style>
        .stApp {
            background-color: #0E1117;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
