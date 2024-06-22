import streamlit as st
import asyncio
import nest_asyncio
from langchain.document_loaders import SitemapLoader


@st.cache_data(show_spinner="Loading website...")
def load_website(url):
    loader = SitemapLoader(url)
    loader.requests_per_second = 1
    documents = loader.load()
    return documents


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
        placeholder="https://example.com",
    )


async def load_documents(url):
    loader = SitemapLoader(url)
    documents = loader.load()
    return documents


if url:
    if ".xml" not in url:
        with st.sidebar:
            st.error("Please write down a Sitemap URL")
    else:
        documents = load_website(url)
