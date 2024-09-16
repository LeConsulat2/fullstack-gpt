import streamlit as st
import asyncio
import nest_asyncio
import os
from langchain.document_loaders import SitemapLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from Utils import check_authentication  # Import the utility function

# Set page configuration for Streamlit
st.set_page_config(
    page_title="Site",
    page_icon="📃",
)


# Ensure the user is authenticated
check_authentication()

# Load environment variables
load_dotenv()

# Access secrets in Streamlit Cloud or locally from environment variables
openai_api_key = (
    os.getenv("OPENAI_API_KEY") or st.secrets["credentials"]["OPENAI_API_KEY"]
)

# Set PATH environment variable if specified in secrets
if "environment" in st.secrets:
    os.environ["PATH"] = st.secrets["environment"]["PATH"]


# Define the page parsing function
def parse_page(soup: BeautifulSoup):
    for element in soup(["header", "footer", "nav", "aside", "script", "style"]):
        element.decompose()
    main_content = soup.find("main")
    text = (
        main_content.get_text(separator="\n", strip=True)
        if main_content
        else soup.get_text(separator="\n", strip=True)
    )
    return str(text).replace("\n", " ").replace("\xa0", " ")


# Function to load and split sitemap data
@st.cache_data(show_spinner="Loading website...")
def load_website(url, limit=100):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=200
    )
    loader = SitemapLoader(
        url, filter_urls=[r"^(.*\/about\/).*"], parsing_function=parse_page
    )  # Adjust filter as needed
    loader.requests_per_second = 2
    docs = loader.load_and_split(text_splitter=splitter)[
        :limit
    ]  # Limit the number of documents
    vector_store = FAISS.from_documents(docs, OpenAIEmbeddings())
    return vector_store.as_retriever()


# Apply nest_asyncio to allow asyncio.run() within an existing event loop
nest_asyncio.apply()

# Set the event loop policy for Windows
if hasattr(asyncio, "WindowsProactorEventLoopPolicy"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Streamlit user interface
st.title("SiteGPT")
st.markdown(
    "Welcome! Use this chatbot to ask questions to an AI about the content of a website! Upload your files on the sidebar."
)

with st.sidebar:
    url = st.text_input(
        "Write down a URL",
        placeholder="https://www.manukau.ac.nz/about/site-help/site-map",
    )

if url:
    if ".xml" not in url:
        with st.sidebar:
            st.error("Please write down a Sitemap URL")
    else:
        documents = load_website(url, limit=100)  # Limit to 100 URLs
        if documents:
            for document in documents:
                st.write(document.page_content)
