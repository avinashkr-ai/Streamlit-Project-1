# Streamlit-Project-1: Simple Stock Price App

A simple Streamlit application to display stock prices. This application fetches stock data using the `yfinance` library and visualizes the historical stock prices using `plotly.graph_objects`.

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

## Features

- Fetches stock data from Yahoo Finance.
- Displays a line chart of the stock's closing price over a period.
- User-friendly interface built with Streamlit.
- Allows users to select a stock ticker and view its historical data.

## Installation

To run this application, you need to install the required dependencies.  It is highly recommended to create a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate  # On Windows

Then, install the dependencies using pip:

```bash
pip install streamlit yfinance plotly

## Usage

To run the application, navigate to the directory containing `streamlit_app.py` and run the following command:

```bash
streamlit run streamlit_app.py

This will open the application in your web browser. You can then enter a stock ticker (e.g., AAPL for Apple) and view its historical stock prices.

## Configuration

No specific configuration files are needed for this project.  The application is self-contained within the `streamlit_app.py` file.

## Contributing

Contributions are welcome! Please feel free to submit pull requests with bug fixes, new features, or improvements to the documentation.

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Code Details

### `streamlit_app.py`

```python
import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.write("""
# Simple Stock Price App

Shown are the stock closing price and volume of Google!
""")

tickerSymbol = st.text_input("Enter Stock Ticker:", "GOOGL")

tickerData = yf.Ticker(tickerSymbol)

tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2023-5-31')

st.write(f"""
## Closing Price Chart for {tickerSymbol}
""")

fig_close = go.Figure(data=[go.Candlestick(x=tickerDf.index,
                open=tickerDf['Open'],
                high=tickerDf['High'],
                low=tickerDf['Low'],
                close=tickerDf['Close'])])

st.plotly_chart(fig_close)


st.write(f"""
## Volume Chart for {tickerSymbol}
""")

fig_volume = go.Figure(data=[go.Bar(x=tickerDf.index, y=tickerDf['Volume'])])
st.plotly_chart(fig_volume)