import streamlit as st
from finance import FinanceTools
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("My Finance Playground")

finance_tools = FinanceTools()

# Find Stock Ticker section
st.markdown("### Find Stock Ticker:")

# Prompt user to input company name
company_name = st.text_input("Enter the name of the company:")

# Display the stock ticker if the company name is provided
if company_name:
    stock_ticker = finance_tools.find_stock_ticker(company_name)
    if stock_ticker:
        st.write(f"{stock_ticker}")
    else:
        st.write(f"Unable to find stock ticker for the company name {company_name}")

# Spacer to separate the sections
st.markdown("---")

# Sidebar for finance tool selection
selected_tool = st.sidebar.radio("Select a tool:", ["Get Stock Prices", "Search News", "Plot Stock Price"])

# Use the selected finance tool based on user input
if selected_tool == "Get Stock Prices":
    # Get Stock Prices section
    st.header("Get Stock Prices")
    # Prompt user to input stock ticker
    stock_ticker_input = st.text_input("Enter a stock ticker:")
    if stock_ticker_input:
        history_length = st.slider("Select length of stock price history (days):", min_value=1, max_value=365, value=30)
        if st.button("Get Stock Prices"):
            df = finance_tools.get_stock_prices(stock_ticker_input, history_length)
            st.write(df)

elif selected_tool == "Search News":
    # Search News section
    st.header("Relevant News")
    # Prompt user to input stock ticker
    stock_ticker_input = st.text_input("Enter a stock ticker:")
    if stock_ticker_input:
        num_articles = st.number_input("Number of articles:", min_value=1, max_value=10, value=5)
        if st.button("Search News"):
            articles_info = finance_tools.search_and_summarize_news(stock_ticker_input, num_articles=num_articles)
            for article_info in articles_info:
                st.write(article_info)

elif selected_tool == "Plot Stock Price":
    # Plot Stock Price section
    st.header("Stock Price Visualization")
    # Prompt user to input stock ticker
    stock_ticker_input = st.text_input("Enter a stock ticker:")
    if stock_ticker_input:
        if st.button("Plot"):
            fig = finance_tools.plot_stock_price(stock_ticker_input)
            st.pyplot(fig)

st.markdown("---")

st.caption("Made by Nam Tran, who created this while possessing the existential dread of someone looking at their 1,000th unanswered job application.")
