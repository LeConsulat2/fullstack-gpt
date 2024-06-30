from langchain.schema import SystemMessage
import streamlit as st
import os
import requests
from typing import Type
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from langchain.agents import initialize_agent, AgentType
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from Dark import set_page_config
from dotenv import load_dotenv
from Utils import check_authentication  # Import the utility function

st.set_page_config(
    page_title="InvestorGPT",
    page_icon="💼",
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


# llm = ChatOpenAI(
#     temperature=0.1,
#     model="gpt-3.5-turbo-0125",
# )


# class StockMarketSymbolSearchToolArgsSchema(BaseModel):
#     query: str = Field(
#         description="The query you will search for.Example query: Stock Market Symbol for Apple Company"
#     )


# class StockMarketSymbolSearchTool(BaseTool):
#     name = "StockMarketSymbolSearchTool"
#     description = """
#     Use this tool to find the stock market symbol for a company.
#     It takes a query as an argument.

#     """
#     args_schema: Type[StockMarketSymbolSearchToolArgsSchema] = (
#         StockMarketSymbolSearchToolArgsSchema
#     )

#     def _run(self, query):
#         ddg = DuckDuckGoSearchAPIWrapper()
#         return ddg.run(query)


# class CompanyOverviewArgsSchema(BaseModel):
#     symbol: str = Field(
#         description="Stock symbol of the company.Example: AAPL,TSLA",
#     )


# class CompanyOverviewTool(BaseTool):
#     name = "CompanyOverview"
#     description = """
#     Use this to get an overview of the financials of the company.
#     You should enter a stock symbol.
#     """
#     args_schema: Type[CompanyOverviewArgsSchema] = CompanyOverviewArgsSchema

#     def _run(self, symbol):
#         r = requests.get(
#             f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={alpha_vantage_api_key}"
#         )
#         return r.json()


# class CompanyIncomeStatementTool(BaseTool):
#     name = "CompanyIncomeStatement"
#     description = """
#     Use this to get the income statement of a company.
#     You should enter a stock symbol.
#     """
#     args_schema: Type[CompanyOverviewArgsSchema] = CompanyOverviewArgsSchema

#     def _run(self, symbol):
#         r = requests.get(
#             f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={alpha_vantage_api_key}"
#         )
#         return r.json()["annualReports"]


# class CompanyStockPerformanceTool(BaseTool):
#     name = "CompanyStockPerformance"
#     description = """
#     Use this to get the weekly performance of a company stock.
#     You should enter a stock symbol.
#     """
#     args_schema: Type[CompanyOverviewArgsSchema] = CompanyOverviewArgsSchema

#     def _run(self, symbol):
#         r = requests.get(
#             f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={alpha_vantage_api_key}"
#         )
#         response = r.json()
#         return list(response["Weekly Time Series"].items())[:200]


# agent = initialize_agent(
#     llm=llm,
#     verbose=True,
#     agent=AgentType.OPENAI_FUNCTIONS,
#     handle_parsing_errors=True,
#     tools=[
#         CompanyIncomeStatementTool(),
#         CompanyStockPerformanceTool(),
#         StockMarketSymbolSearchTool(),
#         CompanyOverviewTool(),
#     ],
#     agent_kwargs={
#         "system_message": SystemMessage(
#             content="""
#             You are a hedge fund manager.

#             You evaluate a company and provide your opinion and reasons why the stock is a buy or not.

#             Consider the performance of a stock, the company overview and the income statement.

#             Be assertive in your judgement and recommend the stock or advise the user against it.
#         """
#         )
#     },
# )


# st.markdown(
#     """
#     # InvestorGPT

#     Welcome to InvestorGPT.

#     Write down the name of a company and our Agent will do the research for you.
# """
# )

# company = st.text_input("Write the name of the company you are interested on.")

# if company:
#     result = agent.invoke(company)
#     st.write(result["output"].replace("$", "\$"))
