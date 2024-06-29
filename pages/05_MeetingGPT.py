import streamlit as st
import subprocess
import math
import os
import glob
import openai
from pydub import AudioSegment
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings  # Updated import
from Dark import set_page_config
import chardet
from dotenv import load_dotenv
from Utils import check_authentication  # Import the utility function

# Ensure the user is authenticated
check_authentication()


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    temperature=0.1,
    model="gpt-3.5-turbo-0125",
)


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
    subprocess.run(command, check=True)


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
        chunk.export(f"{chunks_folder}/openai-devday_{i + 1:02d}.mp3", format="mp3")


has_transcript = os.path.exists("./.cache/openai-devday.txt")


@st.cache_data()  # 폴더 내 모든 청크를 텍스트로 변환
def transcribe_chunks(chunk_folder, destination):
    if has_transcript:
        return
    files = glob.glob(f"{chunk_folder}/*.mp3")
    files.sort()
    final_transcription = ""
    for file in files:
        with open(file, "rb") as audio_file:
            transcription = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
            )
            if hasattr(transcription, "text"):
                final_transcription += transcription.text
            else:
                print(f"Warning: No 'text' attribute in transcription for file {file}")
    with open(destination, "a", encoding="utf-8") as file:  # 기존 파일에 더함
        file.write(final_transcription)


# 경로 설정
audio_path = "./openai-devday.mp3"
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
    with st.status("Loading video...") as status:
        video_content = video.read()
        video_path = f"./.cache/{video.name}"
        audio_path = video_path.replace("mp4", "mp3")
        transcription_path = video_path.replace("mp4", "txt")
        with open(video_path, "wb") as f:
            f.write(video_content)

        status.update(label="Extracting audio...")
        extract_audio_from_video(video_path)

        status.update(label="Cutting audio segments...")
        cut_audio_in_chunks(audio_path, 10, "./.cache/chunks")

        status.update(label="Transcribing audio...")
        transcribe_chunks("./.cache/chunks", transcription_path)

    transcription_tab, summary_tab, qa_tab = st.tabs(
        [
            "Transcript",
            "Summary",
            "Q&A",
        ]
    )

    with transcription_tab:
        try:
            # Detect file encoding
            if not os.path.exists(transcription_path):
                st.error("Transcription file does not exist.")
            else:
                with open(transcription_path, "rb") as raw_file:
                    rawdata = raw_file.read()
                    result = chardet.detect(rawdata)
                    encoding = result["encoding"]

                # Read and display file with detected encoding, ignoring errors
                with open(
                    transcription_path, "r", encoding=encoding, errors="ignore"
                ) as file:
                    content = file.read()
                    st.write(content)
        except Exception as e:
            st.error(f"Error reading file: {e}")

    with summary_tab:
        start = st.button("Generate Summary")

        if start:
            try:
                if not os.path.exists(transcription_path):
                    st.error("Transcription file does not exist.")
                else:
                    # Manually read file content
                    try:
                        with open(
                            transcription_path, "r", encoding=encoding, errors="ignore"
                        ) as file:
                            content = file.read()
                            st.write("Content to be summarized:")
                            st.write(content)
                    except Exception as e:
                        st.error(f"Error reading content: {e}")
                        st.stop()

                    # Use TextLoader to process manually read content
                    try:
                        text_loader = TextLoader(content)
                        # Updated to use SemanticChunker
                        splitter = RecursiveCharacterTextSplitter(
                            OpenAIEmbeddings(api_key=openai_api_key)
                        )
                        docs = splitter.create_documents([content])
                    except Exception as e:
                        st.error(f"Error during load and split: {e}")
                        st.stop()  # Stop further processing if there's an error

                    first_summary_prompt = ChatPromptTemplate.from_template(
                        """
                    Write a concise summary of the following:
                    "{text}"
                    CONCISE SUMMARY:   

                    """
                    )

                    first_summary_chain = first_summary_prompt | llm | StrOutputParser()
                    summary = first_summary_chain.invoke({"text": docs[0].page_content})

                    refine_prompt = ChatPromptTemplate.from_template(
                        """
                        Your job is to produce a final summary.
                        We have provided an existing summary up to a certain point: 
                        {existing_summary}
                        We have the opportunity to refine the existing summary
                        (only if needed) with some more context below.
                        -----------------------------------------------
                        {context}
                        -----------------------------------------------
                        Given the new context, refine the original summary. 
                        If the context isn't useful, RETURN the original summary.

                        """
                    )

                    refine_chain = refine_prompt | llm | StrOutputParser()

                    with st.status("Summarising...") as status:
                        for i, doc in enumerate(docs[1:]):
                            status.update(
                                label=f"Processing document {i + 1}/{len(docs)}"
                            )
                            summary = refine_chain.invoke(
                                {
                                    "existing_summary": summary,
                                    "context": doc.page_content,
                                }
                            )
                    st.write(summary)
            except RuntimeError as e:
                st.error(f"Error processing summary: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
