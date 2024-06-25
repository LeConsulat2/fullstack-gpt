import streamlit as st
import subprocess
import math
import os
import glob
import openai
from pydub import AudioSegment


@st.cache_data()
def extract_audio_from_video(video_path):
    audio_path = video_path.replace("mp4", "mp3")
    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-vn",
        audio_path,
    ]
    subprocess.run(command)


@st.cache_data()  # 오디오 파일을 청크로 나누기
def cut_audio_in_chunks(audio_path, chunk_size, chunks_folder):
    track = AudioSegment.from_mp3(audio_path)  # 오디오 파일 로드
    chunk_length = chunk_size * 60 * 1000  # 청크 크기를 밀리초로 변환
    chunks = math.ceil(len(track) / chunk_length)
    if not os.path.exists(chunks_folder):  # 청크 폴더가 존재하지 않으면 생성
        os.makedirs(chunks_folder)
    for i in range(chunks):  # 각 청크를 개별 파일로 내보내기
        start_time = i * chunk_length
        end_time = (i + 1) * chunk_length
        chunk = track[start_time:end_time]
        chunk.export(f"{chunks_folder}/jocoding-gpt_{i + 1:02d}.mp3", format="mp3")


has_transcript = os.path.exists("./cache/podcast.txt")


@st.cache_data()  # 폴더 내 모든 청크를 텍스트로 변환
def transcribe_chunks(chunk_folder, destination):
    if has_transcript:
        return
    files = glob.glob(f"{chunk_folder}/*.mp3")
    files.sort()
    final_transcription = ""
    for file in files:
        with open(file, "rb") as audio_file:
            transcription = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
            )
            if hasattr(transcription, "text"):
                final_transcription += transcription.text
            else:
                print(f"Warning: No 'text' attribute in transcription for file {file}")
    with open(destination, "w", encoding="utf-8") as file:  # 기존 파일을 덮어씀
        file.write(final_transcription)


# 경로 설정
audio_path = "./jocoding-gpt.mp3"
chunks_folder = "./.cache/chunks"
chunk_size = 10  # 청크 크기 (분 단위)


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
if video:
    with st.status("Loading video..."):
        video_content = video.read()
        video_path = f"./.cache/{video.name}"
        audio_path = video_path.replace("mp4", "mp3")
        transcription_path = video_path.replace("mp4", "txt")
        with open(video_path, "wb") as f:
            f.write(video_content)
    with st.status("Extracting audio..."):
        extract_audio_from_video(video_path)
    with st.status("Cutting audio segments..."):
        cut_audio_in_chunks(audio_path, 10, "./.cache/chunks")
    with st.status("Transcribing audio..."):
        transcribe_chunks("./.cache/chunks", transcription_path)
