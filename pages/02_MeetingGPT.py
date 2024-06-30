import streamlit as st
import subprocess
import os
import openai
from pydub import AudioSegment
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import StrOutputParser
from dotenv import load_dotenv
from Utils import check_authentication  # Import the utility function

st.set_page_config(
    page_title="MeetingGPT",
    page_icon="📃",
)

# Ensure the user is authenticated
check_authentication()

# Load environment variables from .env file for local development
load_dotenv()

# Access secrets in Streamlit Cloud or locally from environment variables
openai_api_key = (
    os.getenv("OPENAI_API_KEY") or st.secrets["credentials"]["OPENAI_API_KEY"]
)
alpha_vantage_api_key = (
    os.getenv("ALPHA_VANTAGE_API_KEY")
    or st.secrets["credentials"]["ALPHA_VANTAGE_API_KEY"]
)
username = os.getenv("username") or st.secrets["credentials"]["username"]
password = os.getenv("password") or st.secrets["credentials"]["password"]

# Set the PATH environment variable from secrets
if "environment" in st.secrets:
    os.environ["PATH"] = st.secrets["environment"]["PATH"]

# Add local FFmpeg binary to the PATH
os.environ["PATH"] += os.pathsep + os.path.abspath("bin/ffmpeg")

st.title("MeetingGPT")

st.markdown(
    """
    ## Welcome to MeetingGPT

    Experience seamless transcription and summary of your meetings with MeetingGPT. 
    
    Upload your video, and we'll provide a detailed transcript, a concise summary, and a chatbot to assist with any queries you might have.

    Get started by uploading a video file via the sidebar.
    """
)

llm = ChatOpenAI(
    temperature=0.1,
    model="gpt-3.5-turbo-0125",
    openai_api_key=openai_api_key,  # Pass the API key here directly
)


def check_ffmpeg_installed():
    try:
        # Check if FFmpeg is accessible
        result = subprocess.run(
            ["ffmpeg", "-version"], check=True, capture_output=True, text=True
        )
        st.write("FFmpeg version output:")
        st.write(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        st.error(f"FFmpeg Error: {e.stderr}")
    except FileNotFoundError:
        st.error("FFmpeg not found.")
    return False


@st.cache_data()  # 폴더 내 모든 청크를 텍스트로 변환
def transcribe_chunks(chunk_folder, destination):
    files = glob.glob(f"{chunk_folder}/*.mp3")
    files.sort()
    for file in files:
        with open(file, "rb") as audio_file, open(
            destination, "a", encoding="utf-8"
        ) as text_file:
            transcription = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
            )
            text_file.write(transcription["text"])


@st.cache_data()
def extract_audio_from_video(video_path):
    audio_path = (
        video_path.replace("mp4", "mp3")
        .replace("avi", "mp3")
        .replace("mkv", "mp3")
        .replace("mov", "mp3")
    )
    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-vn",
        audio_path,
    ]
    try:
        subprocess.run(command, check=True)
        return audio_path
    except subprocess.CalledProcessError as e:
        st.error(f"FFmpeg Error: {e.stderr}")
    except FileNotFoundError as e:
        st.error("FFmpeg not found. Please ensure it is installed and in your PATH.")
    return None


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
        chunk.export(f"{chunks_folder}/{i + 1:02d}.mp3", format="mp3")


with st.sidebar:
    video = st.file_uploader(
        "Upload Video",
        type=["mp4", "avi", "mkv", "mov"],
    )
if video:
    # Ensure the .cache directory exists
    cache_dir = "./.cache"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    video_path = os.path.join(cache_dir, video.name)
    chunks_folder = os.path.join(cache_dir, f"chunks_{os.path.splitext(video.name)[0]}")
    transcription_path = os.path.join(
        cache_dir, f"{os.path.splitext(video.name)[0]}.txt"
    )

    if not os.path.exists(transcription_path):
        with st.status("Loading video...") as status:
            video_content = video.read()
            # Save the uploaded video to a temporary location
            with open(video_path, "wb") as f:
                f.write(video_content)

            if not check_ffmpeg_installed():
                st.error("FFmpeg is not installed. Please install FFmpeg to proceed.")
            else:
                status.update(label="Extracting audio...")
                audio_path = extract_audio_from_video(video_path)
                if audio_path:
                    status.update(label="Cutting audio segments...")
                    cut_audio_in_chunks(audio_path, 10, chunks_folder)
                    status.update(label="Transcribing audio...")
                    transcribe_chunks(chunks_folder, transcription_path)

    transcription_tab, summary_tab, qa_tab = st.tabs(
        [
            "Transcription",
            "Summary",
            "Q&A",
        ]
    )

    with transcription_tab:
        if os.path.exists(transcription_path):
            with open(transcription_path, "r", encoding="utf-8") as file:
                st.write(file.read())
        else:
            st.write("Transcription file not found.")

    with summary_tab:
        start = st.button("Generate summary")

        if start:
            loader = TextLoader(transcription_path)
            splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=800,
                chunk_overlap=100,
            )
            docs = loader.load_and_split(text_splitter=splitter)

            first_summary_prompt = ChatPromptTemplate.from_template(
                """
                Write a concise summary of the following:
                "{text}"
                CONCISE SUMMARY:                
            """
            )

            first_summary_chain = first_summary_prompt | llm | StrOutputParser()

            summary = first_summary_chain.invoke(
                {"text": docs[0].page_content},
            )

            refine_prompt = ChatPromptTemplate.from_template(
                """
                Your job is to produce a final summary.
                We have provided an existing summary up to a certain point: {existing_summary}
                We have the opportunity to refine the existing summary (only if needed) with some more context below.
                ------------
                {context}
                ------------
                Given the new context, refine the original summary.
                If the context isn't useful, RETURN the original summary.
                """
            )

            refine_chain = refine_prompt | llm | StrOutputParser()

            with st.status("Summarizing...") as status:
                for i, doc in enumerate(docs[1:]):
                    status.update(label=f"Processing document {i+1}/{len(docs)-1} ")
                    summary = refine_chain.invoke(
                        {
                            "existing_summary": summary,
                            "context": doc.page_content,
                        }
                    )
                    st.write(summary)
            st.write(summary)
