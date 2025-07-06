import streamlit as st
import json
import re
from src.agents import LangchainStockAgent
from src.tools import get_technical_recommendation as direct_get_recommendation
from src.tools import get_fundamental_analysis as direct_get_fundamentals
from src.tools import get_latest_news_for_summary as direct_get_news
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.messages import AIMessage

def extract_ticker(prompt: str) -> str:
    """Extracts a stock ticker reliably from a prompt."""
    # This corrected regex finds words that are all caps, potentially with a dot.
    matches = re.findall(r'\b[A-Z][A-Z0-9-]{1,9}(?:\.NS|\.BO)?\b', prompt.upper())
    if not matches: return None
    
    # Exclude common non-ticker uppercase words
    non_tickers = ["ANALYSIS", "TECHNICAL", "NEWS", "FUNDAMENTAL", "RECOMMENDATION", "PLEASE", "FOR"]
    matches = [m for m in matches if m not in non_tickers]
    
    if not matches: return None

    # Prefer matches with a '.' as they are explicitly tickers.
    for match in matches:
        if '.' in match:
            return match
            
    # If no ticker with a '.', pick the shortest remaining all-caps word.
    matches.sort(key=len)
    return matches[0]

async def show_stocks_chatbot():
    """Manages the UI using the final HYBRID approach with all features and bug fixes."""
    if "stock_chat_messages" not in st.session_state:
        st.session_state.stock_chat_messages = []

    st.title("📊 Financial Navigator Chatbot")
    st.markdown("Ask for a recommendation, fundamentals, or news.")

    st.markdown("""
    <style>
        .analysis-container { border: 1px solid #e9ecef; border-radius: 12px; padding: 25px; background-color: #ffffff; margin-top: 1em; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
        .analysis-container h4 { color: #0d6efd; border-bottom: 2px solid #f0f2f6; padding-bottom: 10px; margin-top: 0; }
        .analysis-container h5 { margin-top: 20px; margin-bottom: 10px; color: #495057; font-size: 1.1em; }
        .rec-percent { font-size: 1.1em; font-weight: 600; padding: 8px 12px; border-radius: 8px; text-align: center; display: inline-block; margin: 3px; }
        .buy { background-color: #d1e7dd; color: #0f5132; }
        .hold { background-color: #fff3cd; color: #664d03; }
        .sell { background-color: #f8d7da; color: #842029; }
        .verdict-verystrong, .verdict-strong { color: #0f5132; font-weight: 700; }
        .verdict-average { color: #664d03; font-weight: 700; }
        .verdict-weak { color: #842029; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

    current_api_key = st.session_state.get("api_key", ""); current_llm_provider = st.session_state.get("llm_provider", "Groq")
    if not current_api_key: st.warning("Please enter your API key on the login page."); return
    msgs = StreamlitChatMessageHistory(key="stock_chat_messages")

    if "langchain_stock_agent" not in st.session_state or st.session_state.langchain_stock_agent.provider != current_llm_provider:
        with st.spinner("Initializing agent..."):
            st.session_state.langchain_stock_agent = LangchainStockAgent(current_llm_provider, current_api_key)

    for msg in msgs.messages:
        with st.chat_message(msg.type):
            st.markdown(str(msg.content), unsafe_allow_html=True)

    if prompt := st.chat_input("e.g., recommendation for AAPL"):
        msgs.add_user_message(prompt)
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                final_answer = ""; prompt_lower = prompt.lower()
                ticker = extract_ticker(prompt); agent = st.session_state.langchain_stock_agent
                
                if ticker and "news" in prompt_lower:
                    st.info("Getting latest news and AI summary...")
                    tool_output_str = direct_get_news.invoke({"symbol": ticker})
                    tool_output = json.loads(tool_output_str)

                    if tool_output.get("status") == "success":
                        scraped_text = tool_output.get("scraped_text", "")
                        company_name = tool_output.get("company_name")
                        google_link = tool_output.get("google_news_link")

                        if "Could not scrape" not in scraped_text and scraped_text:
                            summary_prompt = f"Provide a concise, 4-5 line summary of the key points from the following news article text about {company_name}:\n\n---\n{scraped_text}\n---"
                            response_obj = await agent.run_agent_with_history(summary_prompt)
                            summary = response_obj.get("output", "Could not summarize the news.")
                            final_answer = f"**AI News Summary for {company_name}:**\n\n{summary}\n\n---\n\nFor more details, [view the latest news on Google]({google_link})."
                        else:
                            final_answer = f"I couldn't retrieve the full article for a summary, but here is a reliable link to the latest news for {company_name}:\n\n[Click here to view on Google News]({google_link})"
                    else: final_answer = f"Sorry, an error occurred: {tool_output.get('message', 'Unknown error')}"
                
                elif ticker and "fundamental" in prompt_lower:
                    st.info("Using direct fundamental analysis tool...")
                    final_answer = direct_get_fundamentals.invoke({"symbol": ticker})

                elif ticker and any(word in prompt_lower for word in ["recommend", "analysis", "analyze", "prediction", "technical"]):
                    st.info("Using direct technical analysis tool...")
                    tool_output_str = direct_get_recommendation.invoke({"symbol": ticker})
                    tool_output = json.loads(tool_output_str)
                    if tool_output.get("status") == "success":
                        text_analysis = tool_output.get("text_analysis", "")
                        rec_percent = tool_output.get("recommendation_percent", {})
                        targets = tool_output.get("price_targets", {})
                        final_answer = f'<div class="analysis-container">'
                        final_answer += f"<h4>📈 Technical Snapshot for {ticker}</h4>"
                        final_answer += f"<h5>Key Signals</h5><p>{text_analysis.replace('•', '<br>•')}</p><hr>"
                        final_answer += f"<h5>Key Price Levels</h5><p><strong>Current:</strong> {targets.get('current', 'N/A')}<br><strong>Support:</strong> {targets.get('support', 'N/A')}<br><strong>Resistance:</strong> {targets.get('resistance', 'N/A')}</p><hr>"
                        final_answer += "<h5>Recommendation</h5>"
                        rec_html = " ".join([f'<span class="rec-percent {cat.lower()}">{cat}: {val}%</span>' for cat, val in rec_percent.items()])
                        final_answer += f"<p>{rec_html}</p>"
                        final_answer += "</div>"
                    else: final_answer = f"Sorry, an error occurred: {tool_output.get('message', 'Unknown error')}"
                
                else: # Fallback
                    st.info("Using AI Agent for conversational response...")
                    response_obj = await agent.run_agent_with_history(prompt)
                    final_answer = response_obj.get("output", "I'm not sure how to help with that.")
                
                st.markdown(final_answer, unsafe_allow_html=True)
                st.markdown("\n*Disclaimer: This information is for educational purposes only.*")
                msgs.add_message(AIMessage(content=final_answer))
