import streamlit as st
import asyncio
import nest_asyncio
from langchain.document_loaders import SitemapLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
import html2text


def parse_page(soup: BeautifulSoup):
    # Exclude common repetitive elements
    for element in soup(["header", "footer", "nav", "aside", "script", "style"]):
        element.decompose()
    # Extract main content
    main_content = soup.find("main")
    if main_content:
        text = main_content.get_text(separator="\n", strip=True)
    else:
        text = soup.get_text(separator="\n", strip=True)
    return str(text).replace("\n", " ").replace("\xa0", " ")  # Non-breaking space


@st.cache_data(show_spinner="Loading website...")
def load_website(url, limit=500):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000,
        chunk_overlap=200,
    )
    loader = SitemapLoader(
        url,
        filter_urls=[
            r"^(.*\/students\/).*",  # Adjust this regex to be more specific if needed
        ],
        parsing_function=parse_page,
    )
    loader.requests_per_second = 2
    docs = loader.load_and_split(text_splitter=splitter)[
        :limit
    ]  # Limit the number of documents
    return docs


# Apply nest_asyncio to allow asyncio.run() within an existing event loop
nest_asyncio.apply()

# Set the event loop policy for Windows
if hasattr(asyncio, "WindowsProactorEventLoopPolicy"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.set_page_config(
    page_title="Site",
    page_icon="📃",
)

st.title("SiteGPT")

st.markdown(
    """
    Welcome!
                
    Use this chatbot to ask questions to an AI about the content of a website!

    Upload your files on the sidebar.
    """
)

with st.sidebar:
    url = st.text_input(
        "Write down a URL",
        placeholder="https://example.com/sitemap.xml",
    )


if url:
    if ".xml" not in url:
        with st.sidebar:
            st.error("Please write down a Sitemap URL")
    else:
        documents = load_website(url, limit=500)  # Limit to 500 URLs
        if documents:
            html2text_transformer = html2text.HTML2Text()
            transformed_documents = [
                html2text_transformer.handle(document.page_content)
                for document in documents
            ]
            for text in transformed_documents:
                st.write(text)
