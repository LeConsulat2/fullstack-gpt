import streamlit as st
import asyncio
import nest_asyncio
import os
from langchain.document_loaders import SitemapLoader
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from bs4 import BeautifulSoup
import html2text
from dotenv import load_dotenv
from Dark import set_page_config
from Utils import check_authentication  # Import the utility function

st.set_page_config(
    page_title="Site",
    page_icon="📃",
)

# Under construction message
st.markdown(
    """
    ## This page is under construction 🔨
    Working on it, once fixed, this page will be up and running for you to use.
"""
)

# Ensure the user is authenticated
check_authentication()

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


# def parse_page(soup: BeautifulSoup):
#     # Exclude common repetitive elements
#     for element in soup(["header", "footer", "nav", "aside", "script", "style"]):
#         element.decompose()
#     # Extract main content
#     main_content = soup.find("main")
#     if main_content:
#         text = main_content.get_text(separator="\n", strip=True)
#     else:
#         text = soup.get_text(separator="\n", strip=True)
#     return str(text).replace("\n", " ").replace("\xa0", " ")  # Non-breaking space


# @st.cache_data(show_spinner="Loading website...")
# def load_website(url, limit=100):
#     splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#         chunk_size=1000,
#         chunk_overlap=200,
#     )
#     loader = SitemapLoader(
#         url,
#         filter_urls=[
#             r"^(.*\/students\/).*",  # Adjust this regex to be more specific if needed
#         ],
#         parsing_function=parse_page,
#     )
#     loader.requests_per_second = 2
#     docs = loader.load_and_split(text_splitter=splitter)[
#         :limit
#     ]  # Limit the number of documents
#     vector_store = FAISS.from_documents(docs, OpenAIEmbeddings())
#     return vector_store.as_retriever()


# # Apply nest_asyncio to allow asyncio.run() within an existing event loop
# nest_asyncio.apply()

# # Set the event loop policy for Windows
# if hasattr(asyncio, "WindowsProactorEventLoopPolicy"):
#     asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


# st.title("SiteGPT")

# st.markdown(
#     """
#     Welcome!

#     Use this chatbot to ask questions to an AI about the content of a website!

#     Upload your files on the sidebar.
#     """
# )

# with st.sidebar:
#     url = st.text_input(
#         "Write down a URL",
#         placeholder="https://example.com/sitemap.xml",
#     )


# if url:
#     if ".xml" not in url:
#         with st.sidebar:
#             st.error("Please write down a Sitemap URL")
#     else:
#         documents = load_website(url, limit=100)  # Limit to 100 URLs
#         if documents:
#             html2text_transformer = html2text.HTML2Text()
#             transformed_documents = [
#                 html2text_transformer.handle(document.page_content)
#                 for document in documents
#             ]
#             for text in transformed_documents:
#                 st.write(text)
