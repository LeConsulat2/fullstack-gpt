import streamlit as st


st.set_page_config(
    page_title="Site",
    page_icon="📃",
)

st.title("MeetingGPT")

st.markdown(
    """
    ## Welcome to MeetingGPT

    Experience seamless transcription and summary of your meetings with MeetingGPT. 
    
    Upload your video, and we'll provide a detailed transcript, a concise summary, and a chatbot to assist with any queries you might have.

    Get started by uploading a video file via the sidebar.
    """
)


with st.sidebar:
    video = st.file_uploader(
        "Video",
        type=["mp4", "avi", "mkv", "mov"],
    )
