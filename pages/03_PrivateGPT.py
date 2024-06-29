from typing import Any, Dict, List
from uuid import UUID
from langchain.prompts import ChatPromptTemplate
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import CacheBackedEmbeddings
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain.storage import LocalFileStore
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.callbacks.base import BaseCallbackHandler
import streamlit as st
from Dark import set_page_config
from dotenv import load_dotenv
import os
import openai

# Load environment variables from .env file
load_dotenv()

# Retrieve the OpenAI API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="PrivateGPT",
    page_icon="📃",
)


class ChatCallBackHandler(BaseCallbackHandler):
    def on_llm_start(self, *args, **kwargs):
        self.message = ""  # Reset message on LLM start
        self.message_box = st.empty()  # Create an empty placeholder for the message

    def on_llm_end(self, *args, **kwargs):
        save_message(self.message, "ai")

    def on_llm_new_token(self, token, *args, **kwargs):
        self.message += token  # Accumulate tokens
        self.message_box.markdown(
            self.message
        )  # Update the message box with the accumulated message


class SimpleMemory:
    def __init__(self):
        self.context = ""

    def update_memory(self, new_context):
        self.context += new_context

    def get_context(self):
        return self.context


if "memory" not in st.session_state:
    st.session_state.memory = SimpleMemory()


class OpenAIEmbeddings:
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(text) for text in texts]

    def embed_text(self, text: str) -> List[float]:
        response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
        return response["data"][0]["embedding"]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_text(text)


@st.cache_resource(show_spinner="Embedding file...")
def embed_file(file):
    file_content = file.read()
    file_path = f"./.cache/private_files/{file.name}"
    with open(file_path, "wb") as f:
        f.write(file_content)
    cache_dir = LocalFileStore(f"./.cache/private_embeddings/{file.name}")
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )
    loader = UnstructuredFileLoader(file_path)
    docs = loader.load_and_split(text_splitter=splitter)

    embeddings = OpenAIEmbeddings()
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)

    # Create a FAISS retriever
    retriever = FAISS.from_documents(docs, cached_embeddings)

    return retriever


def save_message(message, role):
    if "messages" not in st.session_state:  # Ensure session state has a messages list
        st.session_state["messages"] = []
    st.session_state["messages"].append({"message": message, "role": role})


def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        save_message(message, role)


def paint_history():
    if "messages" in st.session_state:  # Check if there are messages in session state
        for message in st.session_state["messages"]:
            send_message(
                message["message"],
                message["role"],
                save=False,
            )


def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)


prompt_template = """
Answer the question using ONLY the following context and not your training data. If you don't know the answer just say you don't know. Don't make anything up.

Context: {context}
Question: {question}
"""

st.title("PrivateGPT")

st.markdown(
    """
    Welcome!
            
    Use this chatbot to ask questions to an AI about your files!

    Upload your files on the sidebar.
    """
)

with st.sidebar:
    file = st.file_uploader(
        "Upload a .txt .pdf or .docx file",
        type=["pdf", "txt", "docx"],
    )

if file:
    retriever = embed_file(file)
    send_message("I'm ready! Ask away!", "ai", save=False)
    paint_history()
    message = st.chat_input("Ask anything about your file...")
    if message:
        send_message(message, "human")
        docs = retriever.similarity_search(message)
        formatted_docs = format_docs(docs)

        # Update memory with the retrieved context
        st.session_state.memory.update_memory(formatted_docs)

        chain_input = {
            "context": st.session_state.memory.get_context(),
            "question": message,
        }

        formatted_prompt = prompt_template.format(**chain_input)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",  # Use the correct model name
            messages=[{"role": "system", "content": formatted_prompt}],
            n=1,
            stop=None,
            temperature=0.1,
        )
        ai_message = response.choices[0].message["content"].strip()
        send_message(ai_message, "ai")
else:
    st.session_state["messages"] = []  # Initialize messages list if not present
