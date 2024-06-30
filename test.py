import os
import streamlit as st
import subprocess

# Print the PATH environment variable to ensure it includes the path to ffmpeg
st.write("System PATH:", os.getenv("PATH"))


def test_ffmpeg():
    command = ["ffmpeg", "-version"]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        st.write("FFmpeg Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        st.error(f"FFmpeg Error: {e.stderr}")
    except FileNotFoundError as e:
        st.error(f"FFmpeg not found: {e}")


st.title("FFmpeg Test")
test_ffmpeg()
