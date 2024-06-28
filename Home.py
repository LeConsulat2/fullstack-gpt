import streamlit as st

# Set the page configuration
st.set_page_config(page_title="AUT GPT HOME", page_icon="💬")


def main():
    # Read query parameters
    query_params = st.query_params

    # Check if the user is authenticated
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.warning("Please log in to access this application")
        st.stop()

    # Check if redirected to home
    if query_params.get("page") == ["home"]:
        st.title("AUT GPT Home")

        # Display markdown content
        st.markdown(
            """
            # Kia Ora!    
            Welcome to AUTGPT Page!

            Here are the apps you can access:

            - []    [DocumentGPT](/DocumentGPT)  
            - []    [PrivateGPT](/PrivateGPT)  
            - []    [QuizGPT](/QuizGPT)  
            - []    [SiteGPT](/SiteGPT)  
            - []    [MeetingGPT](/MeetingGPT)  
            - []    [InvestorGPT](/InvestorGPT)  
            """
        )

        # Create the sidebar with a text input field
        with st.sidebar:
            st.text_input("Question here")


def logout():
    st.session_state.authenticated = False
    st.rerun()


if __name__ == "__main__":
    main()
