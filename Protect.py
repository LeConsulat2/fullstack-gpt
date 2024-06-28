import streamlit as st

# Set the page configuration
st.set_page_config(page_title="AUT GPT Login", page_icon="💬")

# Initialize session state variables if not present
if "page" not in st.session_state:
    st.session_state.page = "login"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


# Function to navigate to a different page
def navigate_to(page):
    st.session_state.page = page
    st.rerun()


# Display the appropriate page based on session state
st.write(f"Current page: {st.session_state.page}")  # Debug statement
st.write(f"Authenticated: {st.session_state.authenticated}")  # Debug statement

if st.session_state.page == "login":
    import Login

    Login.login_page(navigate_to)
elif st.session_state.page == "home":
    import Home

    Home.home_page(navigate_to)
