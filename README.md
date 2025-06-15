Financial Navigator App
Overview
The Financial Navigator is an intelligent Streamlit web application designed to provide users with dynamic insights into stock analysis and personalized SIP (Systematic Investment Plan) recommendations. It leverages large language models (LLMs) orchestrated by langchain.agents to process user queries, execute tools (simulated external data retrieval), and offer reasoned responses and visualizations.

This application is built with modularity in mind, making it easy to understand, maintain, and extend. It demonstrates a robust agentic architecture for building AI-powered financial tools, dynamically adapting to your chosen LLM provider.

Features
Interactive Introduction Page: A visually appealing welcome screen.

Dynamic LLM Selection: Allows users to input their API key and select their preferred LLM provider (Gemini, OpenAI, Groq, HuggingFace, Cohere).

Dynamic Tab Navigation: Seamlessly switch between "Stocks" and "SIP Plan" sections.

Stocks Analysis Chatbot (Agentic AI):

Powered by langchain.agents.AgentExecutor for intelligent reasoning and tool use.

Engage in conversational queries about stock fundamental analysis, price predictions, buy/sell/hold recommendations, and sector-wise analysis.

The LLM dynamically decides which "tool" (e.g., simulated web search, hypothetical stock data fetcher) to call based on the user's query.

Displays hypothetical stock price charts for visualization.

Maintains conversational memory using StreamlitChatMessageHistory.

SIP Plan Recommender:

Takes user preferences (investment goal, risk appetite, horizon, amount) to generate personalized SIP recommendations using direct LLM calls.

Provides structured recommendations with reasoning, suggested duration, and risk levels.

Modular Codebase: Organized into logical Python files for better maintainability.

Attractive UI: Polished with custom CSS for a modern and user-friendly experience.

Project Structure
.
├── app.py                     # Main Streamlit application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── src/                       # Source code directory
    ├── llm_utils.py           # Utility functions for initializing LangChain LLM clients
    ├── tools.py               # Definitions for LangChain-compatible tools
    ├── agents.py              # LangChain Agent Executor setup for stock analysis
    ├── stock_analysis_logic.py# Logic for the Stocks Chatbot feature
    └── sip_planning_logic.py  # Logic for the SIP Planning feature

Setup and Installation
Create Project Directory:
Create a folder named financial-navigator-app. Inside it, create a subfolder named src.

Create Files:
Place the code for requirements.txt, README.md, app.py in the root financial-navigator-app directory.
Place llm_utils.py, tools.py, agents.py, stock_analysis_logic.py, and sip_planning_logic.py inside the src directory.

Create a Virtual Environment (Recommended):
Open your terminal or command prompt, navigate to the financial-navigator-app directory, and run:

python -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`

Install Dependencies:
With your virtual environment activated, run:

pip install -r requirements.txt

API Key:
The application will prompt you for your API key on the login page.

For Gemini, you can typically leave the input empty when running in a Google Canvas environment as the key is provided at runtime. For local testing, you might need to set a GOOGLE_API_KEY environment variable or directly paste it.

For OpenAI, Groq, HuggingFace, or Cohere, you must obtain an API key from their respective developer platforms and paste it into the input field.

How to Run the App
Navigate to the root directory of the project (financial-navigator-app) in your terminal.

Ensure your virtual environment is activated (source venv/bin/activate).

Run the Streamlit application:

streamlit run app.py

Your browser will automatically open to the Streamlit app.

Usage
Introduction Page: Click "Get Started" to proceed.

Login Page: Enter your API key for your chosen LLM provider and select the provider from the radio buttons. Click "Proceed."

Main Application:

Stocks Tab: Engage with the chatbot. Ask questions like:

"What's the fundamental analysis for AAPL?"

"Give me a prediction for TSLA."

"Should I buy, sell, or hold NVDA?"

"Provide sector analysis for the tech sector."
The agent will automatically decide which simulated tool (e.g., google_search_tool, stock_data_fetcher_tool) to use to fulfill your request and provide a comprehensive answer, along with hypothetical charts when relevant.

SIP Plan Tab: Provide your investment preferences using the input fields (investment goal, risk appetite, investment horizon, monthly investment). Click "Generate SIP Plan" to receive structured recommendations tailored to your goals.

Important Notes & Disclaimers
LangGraph Context: While this application uses langchain.agents for an agentic flow with tools and reasoning, it does not implement langgraph's full state machine due to the inherent statelessness of Streamlit's frontend and the typical requirement of a persistent backend for complex langgraph state management. The AgentExecutor provides a robust, agentic conversational experience well-suited for Streamlit.

Simulated Data and Tools: Due to environment constraints, real-time financial data fetching and complex analytical operations are simulated. The "tools" (e.g., Google Search, Stock Data Fetcher) provide predefined or hypothetical responses to demonstrate functionality rather than connecting to live APIs.

Not Financial Advice: All information provided by this application is for educational and informational purposes only and should not be considered financial advice. Always consult with a qualified financial advisor before making any investment decisions.

API Key Security: In a production environment, API keys should never be hardcoded or passed directly in the frontend. Streamlit's secrets management (.streamlit/secrets.toml or environment variables on deployment) is recommended for secure handling.