import streamlit as st


def home_page(navigate_to=None):
    # Standalone check if navigate_to is not provided
    if navigate_to is None:
        # Function to navigate to a different page
        def navigate_to(page):
            st.session_state.page = page
            st.rerun()

    # Check if the user is authenticated
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.warning("Please log in to access this application")
        if st.button("Go to Login page"):
            navigate_to("login")
        st.stop()

    st.title("AUT GPT Home")

    # Display markdown content
    st.markdown(
        """
        # Kia Ora!    
        Welcome to AUTGPT Page!

        Here are the apps you can access:
        """
    )

    # Display the links to the GPT apps only if the user is authenticated
    if st.session_state.authenticated:
        st.markdown(
            """
            - [DocumentGPT](/DocumentGPT)  
            - [PrivateGPT](/PrivateGPT)  
            - [QuizGPT](/QuizGPT)  
            - [SiteGPT](/SiteGPT)  
            - [MeetingGPT](/MeetingGPT)  
            - [InvestorGPT](/InvestorGPT)  
            """
        )
    else:
        st.markdown(
            """
            - DocumentGPT  
            - PrivateGPT  
            - QuizGPT  
            - SiteGPT  
            - MeetingGPT  
            - InvestorGPT  
            """
        )
        st.warning("Please log in to access these applications.")

    # Create the sidebar with a text input field
    # with st.sidebar:
    #     st.text_input("Question here")

    if st.button("Logout"):
        st.session_state.authenticated = False
        navigate_to("login")


# Standalone run check
if __name__ == "__main__":
    home_page()
