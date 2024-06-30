import streamlit as st


def set_page_config(page_title, page_icon):
    st.set_pages_config(
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

        /* Sidebar background */
        .css-1y4p8pa {
            background-color: #0E1117;
        }

        /* Top navigation bar */
        .css-18e3th9 {
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

        /* Adjust all input fields to have dark backgrounds */
        .stTextInput input, .stPasswordInput input, .stSelectbox select, .stTextarea textarea {
            background-color: #333333;
            color: white;
            border: none;
        }

        /* Adjust labels and other text colors */
        .stTextInput label, .stPasswordInput label, .stSelectbox label, .stTextarea label {
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# Example usage
set_page_config("Login Page", ":key:")

# Your login form or other content goes here
st.title("Login")
st.text_input("Username")
st.text_input("Password", type="password")
st.button("Login")
