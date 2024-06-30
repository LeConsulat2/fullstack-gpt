import streamlit as st
from Login import login_page
from Dark import set_pages_config
from Utils import check_authentication  # Import the utility function

# Set the page configuration
st.set_page_config(page_title="AUT GPT Home", page_icon="💬")

# Initialize session state variables if not present
if "page" not in st.session_state:
    st.session_state.page = "login"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


# Function to navigate to a different page
def navigate_to(page):
    st.session_state.page = page
    st.rerun()


def home_page():
    # Check if the user is authenticated
    if not st.session_state.authenticated:
        st.warning("Please log in to access this application")
        if st.button("Go to Login page"):
            navigate_to("login")
        st.stop()

    st.title("AUT GPT Home")

    # Display markdown content
    st.markdown(
        """
        # Kia Ora!    
        Welcome to AUT GPT Page!

        👈Here are the apps you can access from the Side bar👈:
        """
    )

    # Display the links to the GPT apps only if the user is authenticated
    if st.session_state.authenticated:
        st.markdown(
            """
            - DocumentGPT
                         
            - MeetingGPT 

            """
        )
        st.info(
            "🔨  QuizGPT, PrivateGPT,  InvestorGPT,  SiteGPT still under construction...🔨"
        )

    if st.button("Logout"):
        st.session_state.authenticated = False
        navigate_to("login")


# Main app logic to handle navigation
if st.session_state.page == "login":
    login_page(navigate_to)
elif st.session_state.page == "home":
    home_page()
