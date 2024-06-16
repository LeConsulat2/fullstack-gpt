import streamlit as st

st.title("DocumentGPT")

# File uploader
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # To read file as bytes:
    file_content = uploaded_file.read()

    # If you want to display the file content
    st.write(file_content.decode("utf-8"))

    # Optionally, if the file is a text file and you want to process it further
    # Convert bytes to string and process it
    text_content = file_content.decode("utf-8")

    # Display the content
    st.text_area("File Content", text_content, height=300)
