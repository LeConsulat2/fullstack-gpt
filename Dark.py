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
        /* Apply background color to the main container */
        .stApp {
            background-color: #0E1117;
            color: white;
        }
        
        /* Ensure the sidebar is also in dark mode */
        .css-1lcbmhc {
            background-color: #0E1117;
        }

        /* Adjust header text color */
        .css-1q9nb1d h1 {
            color: white;
        }

        /* Adjust main content text color */
        .css-1q9nb1d {
            color: white;
        }

        /* Adjust link color */
        a {
            color: #1f77b4;
        }

        /* Adjust button color */
        .stButton button {
            background-color: #1f77b4;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
