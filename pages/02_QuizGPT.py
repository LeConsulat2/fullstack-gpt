import streamlit as st
from langchain.retrievers import WikipediaRetriever
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
import os

st.set_page_config(
    page_title="QuizGPT",
    page_icon="❓",
)

st.title("QuizGPT")


@st.cache_resource(show_spinner="Loading file...")
def split_file(file):
    file_content = file.read()
    cache_dir = "./.cache/quiz_files"
    os.makedirs(cache_dir, exist_ok=True)
    file_path = os.path.join(cache_dir, file.name)
    with open(file_path, "wb") as f:
        f.write(file_content)

    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )
    loader = UnstructuredFileLoader(file_path)
    docs = loader.load_and_split(text_splitter=splitter)
    return docs


with st.sidebar:
    choice = st.selectbox(
        "Choose what you want to use.",
        (
            "File",
            "Wikipedia Article",
        ),
    )
    if choice == "File":
        file = st.file_uploader(
            "Upload a .docx, .txt or .pdf file",
            type=["pdf", "txt", "docx"],
        )
        if file:
            docs = split_file(file)
            st.write("## Document Contents")
            for doc in docs:
                st.write(doc.page_content)

    else:
        topic = st.text_input("Name of the article")
        if topic:
            retriever = WikipediaRetriever(top_k_results=5)
            with st.spinner("Searching Wikipedia..."):
                documents = retriever.get_relevant_documents(topic)
                st.write("## Relevant Wikipedia Articles")
                for doc in documents:
                    st.write(doc.page_content)
