# 📈 Financial Navigator: AI-Powered Investment Insights

## 🔎 Overview
**Financial Navigator** is an intelligent Streamlit web application that delivers dynamic, real-time stock analysis and personalized SIP (Systematic Investment Plan) recommendations. Built with a hybrid AI architecture, it combines reliable tool-based execution with the advanced reasoning capabilities of Large Language Models (LLMs) to process user queries and provide actionable financial insights.

This solution is designed with a deep focus on:
- ✅ Reliability
- 🌐 User Experience
- ⚖️ In-depth Financial Analysis

---

## ✨ Features
### 🤖 Multi-Provider LLM Integration
- Seamlessly switch between top LLMs like **Groq**, **Gemini**, and **OpenAI** using your API key.

### ⚛️ Hybrid AI Architecture
- Fast-path for direct technical/fundamental analysis
- LangChain ReAct Agent for complex conversational queries

### 🌉 Deep Technical Analysis
- 7+ indicators: SMA Crossovers, RSI, MACD, Bollinger Bands, Volume
- Buy/Sell/Hold recommendations with percentage confidence
- Price targets (Support & Resistance)
- Elegant card-style UI display

### 🏛️ Nuanced Fundamental Analysis
- Metrics: P/E, P/B, PEG, ROE, D/E, Profit Margins, and more
- Weighted scoring to determine: **Very Strong**, **Strong**, **Average**, or **Weak**
- Point-by-point reasoning for every verdict

### 🔔 AI-Powered News Summarization
- Scrapes latest headlines per stock
- AI-generated concise summaries (4-5 lines)
- Direct Google News link for extended reading

### 🌟 Intelligent SIP Planner
- Personalized multi-phase SIP plans
- Future value projections
- Real-world fund examples based on your goals and risk appetite

---

## 🔹 Project Structure with Purpose
```text
financial-navigator-app/
│
├── app.py                     # 🔄 Main Streamlit app that handles routing and UI
├── requirements.txt           # 📦 List of Python libraries required for the app
├── README.md                  # 📘 Project documentation (this file)
│
└── src/                       # 🧠 Core application logic and AI integrations
    ├── llm_utils.py           # ⚙️ Functions to initialize and manage LLM clients
    ├── tools.py               # 🛠️ Financial computation tools (SMA, RSI, etc.)
    ├── agents.py              # 🤖 LangChain ReAct agent setup for chat capabilities
    ├── stock_analysis_logic.py# 📊 Business logic for stock technical/fundamental analysis
    └── sip_planning_logic.py  # 💸 Logic to generate SIP strategy plans and future value
```

---

## 🚀 Setup & Installation

### ✅ Step 1: Create Project Directory
```bash
mkdir financial-navigator-app
cd financial-navigator-app
mkdir src
```

### 📄 Step 2: Add Files
- Place `app.py`, `requirements.txt`, and `README.md` in the root directory
- Place the following files inside `src/`:  
  `llm_utils.py`, `tools.py`, `agents.py`, `stock_analysis_logic.py`, and `sip_planning_logic.py`

### 🧪 Step 3: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 📂 Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 📂 How to Run the App
```bash
cd financial-navigator-app
source venv/bin/activate  # Or venv\Scripts\activate on Windows
streamlit run app.py
```

> Your browser will automatically open the Streamlit app

---

## 💡 Usage Guide

### 📈 Stocks Tab
Chat with the Stock Advisor using questions like:
- "Give me a deep fundamental analysis of HINDUNILVR.NS"
- "I want a technical recommendation and price targets for TATAMOTORS.NS"
- "What is the news summary for AAPL?"

### 🌊 SIP Plan Tab
Input your investment goals and risk appetite. Get:
- Personalized SIP strategy (multi-phase)
- Wealth projections
- Fund suggestions by category

---

## ⚠️ Important Notes & Disclaimers
- **🔒 Not Financial Advice**: Use for educational purposes. Consult a certified advisor before investing.
- **🔍 Live Data**: Market data sourced via `yfinance` may change or become unavailable.
- **🔑 API Key Security**: Store sensitive keys using Streamlit's `.streamlit/secrets.toml` in production.

---

## 💼 Stay Smart, Invest Wisely!
Harness the power of AI to make more informed investment decisions with **Financial Navigator** ✨
