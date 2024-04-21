from llama_index.llms.openai import OpenAI
from llama_index.core.tools.tool_spec.base import BaseToolSpec
from dotenv import load_dotenv
import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta 
from newsapi import NewsApiClient
import matplotlib.dates as mdates
import streamlit as st

NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

llm = OpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)

class FinanceTools(BaseToolSpec):
    """Finance tools class"""
    
    def __init__(self) -> None:
        super().__init__()
        self.newsapi = NewsApiClient(api_key=NEWS_API_KEY)  # Initialize NewsApiClient with provided API key
    
    def get_stock_prices(self, ticker: str, history_length: int) -> pd.DataFrame:
        start_date = date.today() - timedelta(days=history_length)
        end_date = date.today()
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)
        return df
    
    def search_and_summarize_news(self, input_str: str, num_articles:int = 5, from_datetime = date.today() - timedelta(days=5), to_datetime = date.today()):
        # Check if the input is a valid stock ticker
        ticker = input_str if yf.Ticker(input_str).info else self.find_stock_ticker(input_str)
        if not ticker:
            return ["Unable to find stock ticker for the provided input"]

        all_articles = self.newsapi.get_everything(q=ticker,
                                                from_param=from_datetime,
                                                to=to_datetime,
                                                language='en',
                                                sort_by='relevancy',
                                                page_size=num_articles)
        articles_info = []
        for article in all_articles['articles']:
            title = article['title']
            content = article['content']
            # Use LLM to summarize the content of each article
            summary_prompt = f"Summarize: {content}"
            summary = llm.complete(summary_prompt, max_tokens=100).text.strip()
            articles_info.append(f"{title}\n{summary}")

        return articles_info
    
    def find_stock_ticker(self, company_name: str) -> str:
        try:
            # Prompt for finding stock ticker using LLM
            prompt = f"Find the stock ticker symbol for {company_name}."
            response = llm.complete(prompt).text.strip()
            return response
        except Exception as e:
            print(f"An error occurred while finding the stock ticker: {e}")
            return None
    
    
    def plot_stock_price(self, ticker: str) -> plt.figure:
    # Get stock prices
        df = self.get_stock_prices(ticker, 30)
        
        # Calculate daily returns
        df['Daily Return'] = df['Close'].pct_change() * 100
        
        # Plotting
        fig, ax1 = plt.subplots()

        # Plot historical data
        ax1.plot(df.index, df['Close'], color='blue')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price', color='blue')

        # Remove background color for the first axis
        ax1.set_facecolor('none')

        # Create a secondary y-axis for daily returns
        ax2 = ax1.twinx()
        ax2.plot(df.index, df['Daily Return'], color='red')
        ax2.set_ylabel('Daily Return (%)', color='red')

        # Remove background color for the second axis
        ax2.set_facecolor('none')

        # Title and grid
        plt.title(f'{ticker} Historical Data and Daily Returns')
        ax1.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)

        # Set x-axis date format
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

        # Show plot
        plt.tight_layout()
        plt.show()
