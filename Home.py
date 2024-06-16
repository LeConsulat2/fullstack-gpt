import streamlit as st

# Set the page configuration
st.set_page_config(page_title="AUT GPT HOME", page_icon="💬")

# Set the title of the main page
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
- []   [MeetingGPT](/MeetingGPT)  
- []    [InvestorGPT](/InvestorGPT)  
"""
)

# Create the sidebar with a text input field
with st.sidebar:
    st.text_input("Question here")
