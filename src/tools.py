# # src/tools.py
# import json
# import pandas as pd
# import altair as alt
# from langchain.tools import tool
# import yfinance as yf
# import pandas_ta as ta
# import streamlit as st

# def _get_ticker(symbol: str):
#     """Helper to get ticker and check for valid data."""
#     ticker = yf.Ticker(symbol)
#     if ticker.history(period="1d").empty:
#         return None
#     return ticker

# @tool
# def get_technical_recommendation(symbol: str) -> str:
#     """
#     Use this tool to get a full technical analysis and buy/sell/hold recommendation for a stock.
#     This provides a detailed text analysis and automatically prepares a chart for display.
#     Args:
#         symbol (str): The stock ticker. For Indian stocks, use a suffix like .NS (e.g., 'RELIANCE.NS'). For US stocks, use the ticker directly (e.g., 'AAPL').
#     """
#     print(f"DEBUG: Tool 'get_technical_recommendation' called for '{symbol}'")
#     st.session_state['last_chart_spec'] = None # Clear previous chart
#     try:
#         ticker = _get_ticker(symbol)
#         if ticker is None:
#             return f"Error: Invalid or delisted symbol: '{symbol}'. No data found."

#         hist = ticker.history(period="1y")
#         if hist.empty or len(hist) < 200:
#             return f"Error: Not enough historical data for {symbol} to generate a recommendation."

#         df = hist.copy()
#         df.ta.sma(length=50, append=True)
#         df.ta.sma(length=200, append=True)
#         df.ta.rsi(length=14, append=True)
#         df.dropna(inplace=True)

#         if df.empty:
#             return "Error: Could not calculate technical indicators."

#         latest = df.iloc[-1]
#         score = 0
#         reasons = []

#         if latest['SMA_50'] > latest['SMA_200']: score += 2; reasons.append(f"A 'Golden Cross' is active (50-day SMA is above the 200-day SMA), which is a strong bullish signal.")
#         else: score -= 2; reasons.append(f"A 'Death Cross' is active (50-day SMA is below the 200-day SMA), which is a strong bearish signal.")
#         if latest['Close'] > latest['SMA_50']: score += 1; reasons.append(f"The current price is trading above the 50-day SMA, indicating positive short-term momentum.")
#         else: score -= 1; reasons.append(f"The current price is trading below the 50-day SMA, indicating negative short-term momentum.")
#         if latest['RSI_14'] < 30: score += 2; reasons.append(f"The RSI is {latest['RSI_14']:.2f}, indicating the stock may be oversold and undervalued.")
#         elif latest['RSI_14'] > 70: score -= 2; reasons.append(f"The RSI is {latest['RSI_14']:.2f}, indicating the stock may be overbought and overvalued.")

#         text_analysis = "Technical Analysis Summary:\n" + "\n• ".join(reasons)

#         if score >= 3: dist = {"Buy": 75, "Hold": 20, "Sell": 5}
#         elif score >= 1: dist = {"Buy": 60, "Hold": 30, "Sell": 10}
#         else: dist = {"Buy": 25, "Hold": 50, "Sell": 25}

#         pie_df = pd.DataFrame(list(dist.items()), columns=['category', 'value'])
#         chart = alt.Chart(pie_df).mark_arc(innerRadius=50).encode(
#             theta=alt.Theta(field="value", type="quantitative"),
#             color=alt.Color("category:N", title="Recommendation", scale=alt.Scale(domain=['Buy', 'Hold', 'Sell'], range=['#2ca02c', '#ff7f0e', '#d62728'])),
#             tooltip=["category:N", "value:Q"]
#         ).properties(title=f"Recommendation Distribution for {symbol}")
        
#         # Side Effect: Save the chart spec to session state
#         st.session_state['last_chart_spec'] = chart.to_dict()
        
#         return text_analysis # Return only the text analysis

#     except Exception as e:
#         return f"An unexpected error occurred during technical analysis for {symbol}: {e}"

# @tool
# def get_stock_price(symbol: str) -> str:
#     """
#     Use this tool to get the current real-time stock price for a given symbol.
#     Args:
#         symbol (str): The stock ticker (e.g., 'RELIANCE.NS', 'AAPL').
#     """
#     print(f"DEBUG: Tool 'get_stock_price' called for '{symbol}'")
#     try:
#         ticker = _get_ticker(symbol)
#         if ticker is None:
#             return f"Error: Invalid symbol '{symbol}'. Please provide a valid stock ticker."
        
#         price = ticker.history(period="2d")['Close'].iloc[-1]
#         currency = ticker.info.get("currency", "")
#         return f"The current price for {symbol} is {price:,.2f} {currency}."
#     except Exception as e:
#         return f"An error occurred while fetching the price for {symbol}: {e}"



# # src/tools.py
# import json
# import pandas as pd
# import yfinance as yf
# import pandas_ta as ta
# from langchain.tools import tool

# def _get_ticker(symbol: str):
#     """Helper to get ticker and check for valid data."""
#     ticker = yf.Ticker(symbol)
#     if ticker.history(period="1d").empty:
#         return None
#     return ticker

# def _run_technical_analysis(symbol: str):
#     """
#     A helper function to perform text-based technical analysis, including price targets.
#     This version does not generate charts.
#     """
#     ticker = _get_ticker(symbol)
#     if ticker is None:
#         return {"status": "error", "message": f"Invalid or delisted symbol: '{symbol}'. No data found."}

#     hist = ticker.history(period="365d")
#     if hist.empty or len(hist) < 200:
#         return {"status": "error", "message": f"Not enough historical data for {symbol}."}

#     df = hist.copy()
#     df.ta.sma(length=50, append=True, col_names=('SMA50',))
#     df.ta.sma(length=200, append=True, col_names=('SMA200',))
#     df.ta.rsi(length=14, append=True, col_names=('RSI14',))
#     df.dropna(inplace=True)
#     if df.empty: return {"status": "error", "message": "Error calculating indicators."}
    
#     latest = df.iloc[-1]
#     score = 0
#     reasons = []

#     # Simple, clear explanations for each signal
#     if latest['SMA50'] > latest['SMA200']:
#         score += 2
#         reasons.append("• **Golden Cross Active (Bullish):** The short-term average price (50-day) is above the long-term average (200-day), which is a strong positive sign for the trend.")
#     else:
#         score -= 2
#         reasons.append("• **Death Cross Active (Bearish):** The short-term average price is below the long-term average, a negative sign for the trend.")

#     if latest['Close'] > latest['SMA50']:
#         score += 1
#         reasons.append("• **Positive Momentum:** The current price is trading above its 50-day average, indicating recent strength.")
#     else:
#         score -= 1
#         reasons.append("• **Negative Momentum:** The current price is below its 50-day average, indicating recent weakness.")

#     if latest['RSI14'] < 30:
#         score += 2
#         reasons.append(f"• **Potentially Oversold:** The Relative Strength Index (RSI) is {latest['RSI14']:.1f}, suggesting the stock might be undervalued.")
#     elif latest['RSI14'] > 70:
#         score -= 2
#         reasons.append(f"• **Potentially Overbought:** The RSI is {latest['RSI14']:.1f}, suggesting the stock may be overvalued.")
#     else:
#         reasons.append(f"• **Neutral RSI:** The RSI is {latest['RSI14']:.1f}, indicating a balanced momentum.")
    
#     text_analysis = "\n".join(reasons)

#     # Determine percentage-based recommendation
#     if score >= 3: dist = {"Buy": 75, "Hold": 20, "Sell": 5}
#     elif score >= 1: dist = {"Buy": 60, "Hold": 30, "Sell": 10}
#     else: dist = {"Buy": 25, "Hold": 50, "Sell": 25}
    
#     # Calculate Support and Resistance for Price Targets
#     recent_data = df.tail(60) # Use last 60 days for recent levels
#     support_level = recent_data['Low'].min()
#     resistance_level = recent_data['High'].max()
    
#     price_targets = {
#         "support": f"₹{support_level:,.2f}",
#         "resistance": f"₹{resistance_level:,.2f}",
#         "current": f"₹{latest['Close']:,.2f}"
#     }

#     return {
#         "status": "success",
#         "text_analysis": text_analysis,
#         "recommendation_percent": dist,
#         "price_targets": price_targets
#     }

# @tool
# def get_technical_recommendation(symbol: str) -> str:
#     """Use this tool for a full technical analysis and buy/sell/hold recommendation for a SINGLE stock."""
#     try:
#         result = _run_technical_analysis(symbol)
#         return json.dumps(result)
#     except Exception as e:
#         return json.dumps({"status": "error", "message": f"An unexpected error occurred: {e}"})

# @tool
# def get_fundamental_analysis(symbol: str) -> str:
#     """Use this tool to get key fundamental data for a company. The AI will then analyze this data to judge if the fundamentals are strong or not."""
#     try:
#         ticker = _get_ticker(symbol)
#         if ticker is None: return "Error: Invalid or delisted symbol."
#         info = ticker.info
#         fundamentals = {
#             "Company Name": info.get("longName"), "Sector": info.get("sector"),
#             "Market Cap": f"{info.get('marketCap', 0):,}", "Trailing P/E Ratio": info.get("trailingPE"),
#             "Debt to Equity Ratio": info.get("debtToEquity"), "Return on Equity": info.get("returnOnEquity"),
#         }
#         return "Fundamental Data for AI analysis:\n" + "\n".join([f"- {key}: {value}" for key, value in fundamentals.items() if value is not None])
#     except Exception as e:
#         return f"An error occurred during fundamental analysis for {symbol}: {e}"

# src/tools.py - GRAND FINALE VERSION
import json
import pandas as pd
import yfinance as yf
import pandas_ta as ta
from langchain.tools import tool
from pydantic import BaseModel, Field
import urllib.parse
import requests
from bs4 import BeautifulSoup

class StockSymbolInput(BaseModel):
    """Input model for tools that require a stock symbol."""
    symbol: str = Field(description="The stock ticker symbol. For Indian stocks, use a suffix like .NS. For US stocks, use the ticker directly.")

def _get_ticker(symbol: str):
    """Helper to get ticker and check for valid data."""
    ticker = yf.Ticker(symbol)
    if ticker.history(period="1d").empty:
        return None, None
    info = ticker.info
    return ticker, info

@tool("get_technical_recommendation", args_schema=StockSymbolInput)
def get_technical_recommendation(symbol: str) -> str:
    """Use this tool for a full, deep technical analysis and buy/sell/hold recommendation for a SINGLE stock."""
    try:
        ticker, info = _get_ticker(symbol)
        if ticker is None: return json.dumps({"status": "error", "message": f"Invalid symbol: '{symbol}'."})
        hist = ticker.history(period="1y")
        if hist.empty or len(hist) < 200: return json.dumps({"status": "error", "message": f"Not enough data for {symbol}."})

        # --- 1. Calculate All Technical Indicators ---
        df = hist.copy()
        df.ta.sma(length=50, append=True, col_names=('SMA50',))
        df.ta.sma(length=200, append=True, col_names=('SMA200',))
        df.ta.rsi(length=14, append=True, col_names=('RSI14',))
        df.ta.macd(append=True, col_names=('MACD', 'MACDh', 'MACDs'))
        df.ta.bbands(append=True, col_names=('BBL', 'BBM', 'BBU', 'BBB', 'BBP'))
        df.dropna(inplace=True)
        if df.empty: return json.dumps({"status": "error", "message": "Error calculating indicators."})
        
        latest = df.iloc[-1]; score = 0; reasons = []

        # --- 2. Analyze Indicators with More Detail ---
        if latest['SMA50'] > latest['SMA200']: score += 2; reasons.append("• **Trend is Bullish:** A 'Golden Cross' is active.")
        else: score -= 2; reasons.append("• **Trend is Bearish:** A 'Death Cross' is active.")
        if latest['Close'] > latest['SMA50']: score += 1; reasons.append("• **Momentum is Positive:** Price is above the 50-day average.")
        else: score -= 1; reasons.append("• **Momentum is Negative:** Price is below the 50-day average.")
        if latest['RSI14'] < 30: score += 2; reasons.append(f"• **Potentially Oversold:** RSI is {latest['RSI14']:.1f}.")
        elif latest['RSI14'] > 70: score -= 2; reasons.append(f"• **Potentially Overbought:** RSI is {latest['RSI14']:.1f}.")
        if latest['MACD'] > latest['MACDs']: score += 1; reasons.append("• **MACD indicates Bullish momentum.**")
        else: score -=1; reasons.append("• **MACD indicates Bearish momentum.**")
        
        avg_volume = df['Volume'].tail(20).mean()
        if latest['Volume'] > avg_volume * 1.5: reasons.append(f"• **Volume is High:** Recent volume confirms trend strength.")
        
        text_analysis = "\n".join(reasons)

        if score >= 5: dist = {"Buy": 80, "Hold": 15, "Sell": 5}
        elif score >= 3: dist = {"Buy": 70, "Hold": 25, "Sell": 5}
        elif score >= 1: dist = {"Buy": 60, "Hold": 30, "Sell": 10}
        else: dist = {"Buy": 20, "Hold": 60, "Sell": 20}
        
        recent_data = df.tail(90); support_level = recent_data['Low'].min(); resistance_level = recent_data['High'].max()
        price_targets = {"support": f"₹{support_level:,.2f}", "resistance": f"₹{resistance_level:,.2f}", "current": f"₹{latest['Close']:,.2f}"}

        return json.dumps({"status": "success", "text_analysis": text_analysis, "recommendation_percent": dist, "price_targets": price_targets})
    except Exception as e: return json.dumps({"status": "error", "message": f"An unexpected error occurred: {e}"})

@tool("get_fundamental_analysis", args_schema=StockSymbolInput)
def get_fundamental_analysis(symbol: str) -> str:
    """Use this tool to get a full, detailed fundamental analysis report for a company, including many key metrics."""
    try:
        ticker, info = _get_ticker(symbol)
        if ticker is None: return "Error: Invalid or delisted symbol."
        
        pe = info.get("trailingPE"); roe = info.get("returnOnEquity"); de = info.get("debtToEquity")
        ps = info.get("priceToSalesTrailing12Months"); peg = info.get("pegRatio"); sector = info.get("sector", "")
        pb = info.get("priceToBook"); margins = info.get("profitMargins")
        
        positive_points = []; caution_points = []; score = 0
        if info.get('marketCap'): positive_points.append(f"• **Market Cap:** A large cap of {info.get('marketCap', 0):,} indicates a stable business.")
        if pe is not None and pe < 25: positive_points.append(f"• **Valuation (P/E of {pe:.2f}):** Appears reasonably valued."); score += 1
        elif pe is not None: caution_points.append(f"• **Valuation (P/E of {pe:.2f}):** P/E ratio is high."); score -= 1
        if peg is not None and 0 < peg < 1: positive_points.append(f"• **Growth vs. Price (PEG of {peg:.2f}):** Excellent PEG ratio suggests potential undervaluation."); score += 2
        if roe is not None and roe > 0.15: positive_points.append(f"• **Profitability (ROE of {roe:.2%}):** Strong ROE indicates efficient profit generation."); score += 2
        else: caution_points.append(f"• **Profitability (ROE of {roe if roe is not None else 'N/A'}):** ROE is on the lower side.")
        if de is not None and de < 1.0: positive_points.append(f"• **Financial Health (D/E of {de:.2f}):** Has a manageable level of debt."); score += 1
        else: caution_points.append(f"• **Financial Health (D/E of {de if de is not None else 'N/A'}):** Holds a significant level of debt."); score -= 1
        if pb is not None and pb < 3: positive_points.append(f"• **Book Value (P/B of {pb:.2f}):** A P/B ratio under 3 can indicate good value."); score += 1
        if ps is not None and ps < 2: positive_points.append(f"• **Sales Valuation (P/S of {ps:.2f}):** A low Price-to-Sales ratio is a positive sign."); score += 1
        if margins is not None and margins > 0.1: positive_points.append(f"• **Margins (Profit Margin of {margins:.2%}):** Healthy profit margins show a strong business model."); score += 1
        
        if not positive_points: positive_points.append("• No specific positive indicators found.")
        if not caution_points: caution_points.append("• No specific points of caution found.")
        
        if score >= 5: final_verdict = "Very Strong"
        elif score >= 3: final_verdict = "Strong"
        elif score >= 1: final_verdict = "Average"
        else: final_verdict = "Weak"
        
        response_html = f'<div class="analysis-container">'
        response_html += f"<h4>Fundamental Snapshot for {info.get('longName', symbol)}</h4><hr>"
        response_html += "<h6>Positive Points:</h6>"; response_html += f"<p>{'<br>'.join(positive_points)}</p>"
        response_html += "<h6>Points of Caution:</h6>"; response_html += f"<p>{'<br>'.join(caution_points)}</p><hr>"
        verdict_class = f"verdict-{final_verdict.lower().replace(' ', '')}"
        response_html += f'<h5>Final Verdict: <span class="{verdict_class}">{final_verdict} Fundamentals</span></h5>'
        response_html += '</div>'
        return response_html
    except Exception as e: return f"An error occurred during fundamental analysis for {symbol}: {e}"

@tool("get_latest_news_for_summary", args_schema=StockSymbolInput)
def get_latest_news_for_summary(symbol: str) -> str:
    """Gets the latest news for a stock, scrapes the top article, and returns its content for an AI to summarize."""
    try:
        ticker, info = _get_ticker(symbol)
        if ticker is None: return json.dumps({"status": "error", "message": "Invalid symbol."})
        company_name = info.get('longName', symbol)
        
        query = f"{company_name} stock news"; encoded_query = urllib.parse.quote_plus(query)
        google_url = f"https://news.google.com/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
        headers = { 'User-Agent': 'Mozilla/5.0' }
        r = requests.get(google_url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        
        article_text = "Could not scrape the full article content."
        first_link_tag = soup.find('a', class_='JtKRv')
        
        if first_link_tag and first_link_tag.get('href'):
            article_url = urllib.parse.urljoin("https://news.google.com", first_link_tag['href'])
            try:
                article_r = requests.get(article_url, headers=headers, timeout=5)
                article_soup = BeautifulSoup(article_r.text, 'lxml')
                paragraphs = article_soup.find_all('p')
                full_text = " ".join([p.text for p in paragraphs])
                article_text = full_text[:2500] + "..." if len(full_text) > 2500 else full_text
            except Exception as e:
                print(f"DEBUG: Failed to scrape article content: {e}")

        return json.dumps({
            "status": "success", "google_news_link": google_url,
            "company_name": company_name, "scraped_text": article_text
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": f"An error occurred while fetching news: {e}"})
