import streamlit as st
from langchain.retrievers import WikipediaRetriever
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain_community.chat_models import ChatOpenAI
import os

st.set_page_config(
    page_title="QuizGPT",
    page_icon="❓",
)

st.title("QuizGPT")

llm = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo-0125")


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


docs = None

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

if not docs:
    st.markdown(
        """
    Welcome to QuizGPT.

    I will make a quiz from the AUT website, Calendar, knowledge base articles or files you upload to test your knowledge and help you learn.

    Get started by uploading a file or searching on Wikipedia in the sidebar!


    """
    )
else:
    st.write(docs)
