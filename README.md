Financial Navigator: AI-Powered Investment Insights
Overview
The Financial Navigator is an intelligent Streamlit web application designed to provide users with dynamic, real-time insights into stock analysis and personalized SIP (Systematic Investment Plan) recommendations. It leverages a sophisticated hybrid architecture, combining direct, reliable tool execution with the advanced reasoning of Large Language Models (LLMs) to process user queries and offer clear, actionable financial intelligence.

This application has been built from the ground up with a focus on reliability, user experience, and providing deep, nuanced analysis that goes beyond simple data retrieval.

Features
Dynamic, Multi-Provider LLM Core: Seamlessly switch between top-tier LLM providers like Groq, Gemini, and OpenAI by simply providing your API key.

Hybrid AI Architecture: For maximum speed and reliability, common requests for technical or fundamental analysis are handled by direct, "fast-path" tool calls. More complex, conversational queries are handled by a robust LangChain ReAct agent.

Deep Technical Analysis:

Goes beyond simple indicators by analyzing a suite of 7+ technical metrics, including SMA Crossovers (Golden/Death Cross), RSI, MACD, Bollinger Bands, and Volume.

Provides a clear, percentage-based Buy/Sell/Hold recommendation.

Calculates and displays dynamic Price Targets (Support and Resistance) to inform entry and exit strategies.

Presents all information in a polished, decorative "card" UI for an excellent user experience.

Nuanced Fundamental Analysis:

Analyzes a deep "matrix" of 7+ key financial metrics, including P/E, P/B, PEG Ratio, ROE, D/E, and Profit Margins.

Provides a final verdict of "Very Strong," "Strong," "Average," or "Weak" based on a weighted scoring of the metrics.

Delivers a detailed, point-by-point explanation of the positive factors and points of caution for each company.

AI-Powered News Summary:

Fetches the latest news for any stock by scraping top headlines.

Uses an AI agent to generate a concise, 4-5 line summary of the key themes from the news.

Always provides a reliable, direct link to Google News for further reading.

Intelligent SIP Planner:

Generates personalized, multi-phase SIP strategies based on your unique goals and risk appetite.

Includes a Future Value Calculator to project your potential wealth over time.

Suggests well-known, real-world mutual funds as illustrative examples for each recommended category.

Project Structure
.
├── app.py                     # Main Streamlit application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── src/                       # Source code directory
    ├── llm_utils.py           # Utility functions for initializing LLM clients
    ├── tools.py               # Definitions for all financial analysis tools
    ├── agents.py              # LangChain ReAct Agent setup
    ├── stock_analysis_logic.py# Logic for the Stock Analysis Chatbot
    └── sip_planning_logic.py  # Logic for the SIP Planning feature

Setup and Installation
1. Create Project Directory:
Create a folder named financial-navigator-app. Inside it, create a subfolder named src.

2. Create Files:
Place the code for requirements.txt, README.md, and app.py in the root financial-navigator-app directory. Place llm_utils.py, tools.py, agents.py, stock_analysis_logic.py, and sip_planning_logic.py inside the src directory.

3. Create a Virtual Environment (Recommended):
Open your terminal, navigate to the financial-navigator-app directory, and run:

python -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`

4. Install Dependencies:
With your virtual environment activated, ensure your requirements.txt is up-to-date and run:

pip install -r requirements.txt

How to Run the App
Navigate to the root directory of the project (financial-navigator-app) in your terminal.

Ensure your virtual environment is activated.

Run the Streamlit application:

streamlit run app.py

Your browser will automatically open to the Streamlit app.

Usage
Stocks Tab: Engage with the chatbot. Ask questions like:

"Give me a deep fundamental analysis of HINDUNILVR.NS"

"I want a technical recommendation and price targets for TATAMOTORS.NS"

"What is the news summary for AAPL?"

SIP Plan Tab: Provide your investment preferences to receive a detailed, multi-phase investment strategy with fund examples and wealth projections.

Important Notes & Disclaimers
Not Financial Advice: All information provided by this application is for educational and informational purposes only and should not be considered financial advice. Always consult with a qualified financial advisor before making any investment decisions.

Live Data: The application uses the yfinance library to fetch near real-time market data. Data accuracy and availability are dependent on the source.

API Key Security: In a production environment, API keys should be handled securely using Streamlit's secrets management (`.streamlit