import pandas as pd
import numpy as np
import altair as alt
import json
from langchain_core.tools import tool # Import the tool decorator

@tool
def google_search_tool(query: str) -> str:
    """
    Performs a simulated Google Search for financial information.
    Use this for general web searches, news, analyst reports, sector analysis, or detailed
    fundamental/prediction insights not covered by simple data fetching.
    """
    print(f"DEBUG: Simulating Google Search for: {query}") # Debug print

    query_lower = query.lower()
    if "apple stock fundamental analysis" in query_lower or "aapl fundamental analysis" in query_lower:
        return """
        Search Result (Google): Apple Inc. (AAPL) is a tech giant known for its strong brand, ecosystem, and services growth.
        Fundamental analysis highlights:
        - Revenue: Diversified across iPhone, Services, Mac, iPad, Wearables. Services segment is a key growth driver.
        - Profitability: Consistently high gross and operating margins. Strong free cash flow generation.
        - Balance Sheet: Large cash reserves, though often offset by debt for share buybacks.
        - Valuation: P/E ratios are typically higher than the S&P 500 average due to its growth and stability.
        - Analyst Sentiment: Generally positive, focusing on continued ecosystem expansion and new product categories (e.g., Vision Pro).
        - Risks: Supply chain disruptions, reliance on iPhone sales, regulatory scrutiny, intense competition.
        """
    elif "tesla stock prediction" in query_lower or "tsla stock prediction" in query_lower:
        return """
        Search Result (Google): Tesla (TSLA) stock is highly volatile.
        Prediction factors:
        - EV Market Growth: Global adoption trends.
        - Production & Deliveries: Quarterly numbers are critical indicators.
        - Competition: Increasing competition from traditional automakers and new EV players.
        - FSD (Full Self-Driving) Progress: Key long-term driver, but regulatory hurdles exist.
        - Elon Musk's Influence: Public statements and actions significantly impact stock price.
        - Technical Indicators: Moving Averages (e.g., 50-day SMA, 200-day SMA) are watched. A 50-day SMA crossing above 200-day SMA (Golden Cross) is bullish, below (Death Cross) is bearish.
        - Analyst Views: Wide range of price targets; some are bullish on AI and robotaxi, others cautious on valuation and delivery miss risks.
        """
    elif "nvidia stock performance" in query_lower or "nvda stock performance" in query_lower:
        return """
        Search Result (Google): Nvidia (NVDA) has experienced massive growth due to its dominance in AI chips.
        Performance insights:
        - Data Center Segment: Primary growth driver, fueled by demand for AI/ML GPUs.
        - Gaming: Strong segment, but can be cyclical.
        - Financials: Exceptional revenue growth, high gross margins, significant R&D investment.
        - Competitive Landscape: While dominant, faces competition from custom silicon (e.g., Google's TPUs, AWS Trainium) and AMD.
        - Valuation: Very high P/E ratios reflecting high growth expectations.
        - Analyst Sentiment: Overwhelmingly bullish due to AI tailwinds.
        - Risks: Geopolitical tensions affecting chip supply, potential slowdown in AI infrastructure spending, competition.
        """
    elif "buy sell or hold" in query_lower:
        # For buy/sell/hold, provide general analyst consensus
        return """
        Search Result (Google): General analyst consensus for many well-known stocks tends to be 'Hold' or 'Buy' with specific price targets.
        'Buy' implies expected outperformance. 'Hold' suggests neutral expectations or waiting for clear catalysts. 'Sell' implies expected underperformance.
        Recommendations are based on fundamental outlook, technical analysis, and market conditions.
        """
    elif "tech sector analysis" in query_lower:
        return """
        Search Result (Google): The technology sector is broad, encompassing software, hardware, semiconductors, and internet services.
        Key trends: Artificial Intelligence (AI) adoption, cloud computing expansion, cybersecurity demand, digital transformation, and 5G integration.
        Growth Drivers: Innovation, R&D, global digitalization.
        Risks: Regulatory scrutiny, intense competition, supply chain issues, talent shortages, economic downturns impacting enterprise spending.
        Sub-sectors: Software as a Service (SaaS), Semiconductors, Cloud Infrastructure, E-commerce, Fintech.
        """
    elif "best sip plans for retirement" in query_lower or "sip for long term" in query_lower:
        return """
        Search Result (Google): For long-term goals like retirement (15+ years), equity-oriented SIPs are generally recommended.
        - Categories: Large-cap, Multi-cap, Flexi-cap, Index Funds.
        - Reasoning: Higher growth potential over long periods to beat inflation. Diversification across market capitalizations.
        - Considerations: Expense ratio, fund manager's track record, volatility in short-to-medium term.
        - Hybrid funds: Can be considered for moderate risk appetite, balancing equity and debt.
        """
    elif "short-term sip plans" in query_lower or "sip for 1-3 years" in query_lower:
        return """
        Search Result (Google): For short-term goals (1-3 years), equity SIPs are generally not recommended due to high volatility.
        - Categories: Debt funds (e.g., Ultra-short duration funds, Liquid funds).
        - Reasoning: Prioritize capital preservation and stability over high returns. Less susceptible to market fluctuations.
        - Considerations: Lower returns compared to equities, but safer for short horizons.
        """
    else:
        return f"Search Result (Google): Found various financial news outlets, company reports, and investment analysis websites for '{query}'. Please specify your query more precisely for a more targeted search. No specific detailed information found for this exact query pattern in our simulated data."

@tool
def stock_data_fetcher_tool(symbol: str, period_days: int = 100) -> str:
    """
    Simulates fetching hypothetical historical stock price data for a given symbol.
    Returns a JSON string representing hypothetical stock data suitable for charting.
    The `symbol` argument is the stock ticker (e.g., 'AAPL', 'TSLA').
    The `period_days` argument specifies the number of days for which to fetch data (default is 100).
    """
    print(f"DEBUG: Simulating stock data fetch for: {symbol} for {period_days} days.") # Debug print

    # Generate hypothetical data
    dates = pd.date_range(end=pd.Timestamp.now(), periods=period_days, freq='D')
    # Start price, trend, and volatility
    base_price = 100 + (len(symbol) * 5) # Varies slightly by symbol length
    price_series = np.cumsum(np.random.normal(loc=0.1, scale=0.5, size=period_days)) + base_price
    prices = np.maximum(price_series, base_price * 0.9) # Ensure prices don't drop too low

    data = pd.DataFrame({"Date": dates, "Price": prices})
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d') # Format date for JSON

    return json.dumps(data.to_dict(orient="records"))

# This is a helper function for Streamlit display, not a tool for the agent.
def chart_generator_tool(data_json: str, title: str) -> alt.Chart:
    """
    Generates an Altair chart from JSON stock data.
    """
    data = pd.DataFrame(json.loads(data_json))
    data['Date'] = pd.to_datetime(data['Date']) # Convert back to datetime for Altair

    chart = alt.Chart(data).mark_line(point=True).encode(
        x=alt.X("Date:T", title="Date"),
        y=alt.Y("Price:Q", title="Price"),
        tooltip=[alt.Tooltip("Date:T", format="%Y-%m-%d"), "Price:Q"]
    ).properties(
        title=f"Hypothetical Stock Price for {title}"
    ).interactive() # Allows zooming and panning

    return chart

