import streamlit as st
import asyncio
from src.agents import LangchainStockAgent # Import the new LangChain agent
from src.tools import chart_generator_tool # Import the tool to generate charts (still used for display)
from langchain_community.chat_message_histories import StreamlitChatMessageHistory # For persistent chat history
from langchain_core.messages import HumanMessage, AIMessage

async def show_stocks_chatbot():
    """
    Manages the Streamlit UI for the stock analysis chatbot,
    integrating the LangchainStockAgent for dynamic responses and tool usage.
    """
    st.subheader("📊 Stock Analysis Chatbot")

    # Get API key and provider from session state
    current_api_key = st.session_state.get("api_key", "")
    current_llm_provider = st.session_state.get("llm_provider", "Gemini")

    if not current_api_key:
        st.warning("Please enter your API key on the login page to use the chatbot.")
        return

    # Initialize StreamlitChatMessageHistory for persistent chat history
    # This automatically syncs with st.session_state
    msgs = StreamlitChatMessageHistory(key="stock_chat_messages")

    # Initialize the LangChain agent with the selected LLM
    if "langchain_stock_agent" not in st.session_state or \
       st.session_state.langchain_stock_agent.provider != current_llm_provider or \
       st.session_state.langchain_stock_agent.api_key != current_api_key:
        try:
            st.session_state.langchain_stock_agent = LangchainStockAgent(current_llm_provider, current_api_key)
        except ValueError as e:
            st.error(f"Failed to initialize agent: {e}")
            return

    # Display chat messages from history
    for msg in msgs.messages:
        # LangChain messages have 'type' (human, ai, system, etc.)
        # Streamlit chat_message expects 'user' or 'assistant'.
        st_chat_role = "user" if msg.type == "human" else "assistant"
        with st.chat_message(st_chat_role):
            st.markdown(msg.content)
            # If a chart was previously generated, display it
            if hasattr(msg, 'additional_kwargs') and 'chart_data' in msg.additional_kwargs:
                try:
                    chart = chart_generator_tool(msg.additional_kwargs['chart_data'], msg.additional_kwargs.get('chart_title', 'Stock'))
                    st.altair_chart(chart, use_container_width=True)
                    st.caption("Note: This chart uses hypothetical data for demonstration purposes only, as real-time stock data fetching is not integrated in this demo environment.")
                except Exception as e:
                    st.error(f"Error displaying historical chart: {e}")


    # Chat input for user
    if prompt := st.chat_input("Ask me about stocks (e.g., 'fundamental analysis for AAPL', 'prediction for TSLA', 'sector analysis for tech')"):
        # Add user message to LangChain history and display
        msgs.add_user_message(prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get assistant response using the LangChain agent
        with st.chat_message("assistant"):
            with st.spinner(f"Analyzing with {current_llm_provider}..."):
                try:
                    # Run the agent's invoke method
                    # The `ainvoke` method runs the agent's logic, including tool calls.
                    # The chat history is passed via the prompt template's MessagesPlaceholder.
                    # This will automatically use the `msgs.messages` from StreamlitChatMessageHistory.
                    agent_response_obj = await st.session_state.langchain_stock_agent.agent_executor.ainvoke(
                        {"input": prompt, "chat_history": msgs.messages}
                    )
                    
                    response_content = agent_response_obj.get("output", "I could not generate a response.")
                    st.markdown(response_content)

                    # Check if a tool call was made that results in chart data (from our simulated tools)
                    chart_metadata = {}
                    if "tool_calls" in agent_response_obj and agent_response_obj["tool_calls"]:
                        for tool_call in agent_response_obj["tool_calls"]:
                            if tool_call["name"] == "stock_data_fetcher_tool":
                                # This is a placeholder. In a real scenario, the tool output needs to be passed back
                                # through the agent's response, or a separate mechanism to trigger chart display.
                                # For this simplified AgentExecutor, we'll assume the LLM's final response will signal
                                # when a chart should be displayed and we'll manually fetch and display it here
                                # if the tool was implicitly called.
                                # A better approach would involve structured output from the agent including chart data.
                                # For now, let's re-fetch data based on the prompt's implied symbol for chart display.
                                import re
                                match = re.search(r'(?i)(AAPL|TSLA|NVDA)', prompt) # Simple regex to find symbol
                                if match:
                                    symbol = match.group(0).upper()
                                    try:
                                        from src.tools import stock_data_fetcher_tool as direct_fetch_tool
                                        chart_data_json = direct_fetch_tool(symbol)
                                        chart = chart_generator_tool(chart_data_json, symbol)
                                        st.altair_chart(chart, use_container_width=True)
                                        st.caption("Note: This chart uses hypothetical data for demonstration purposes only, as real-time stock data fetching is not integrated in this demo environment.")
                                        # Store chart metadata to display on rerun (important for Streamlit)
                                        chart_metadata = {"chart_data": chart_data_json, "chart_title": symbol}
                                    except Exception as chart_e:
                                        st.error(f"Error generating chart: {chart_e}")


                    # Add assistant response to LangChain history
                    # We append additional_kwargs for chart data for persistence across reruns
                    if chart_metadata:
                        msgs.add_ai_message(AIMessage(content=response_content, additional_kwargs=chart_metadata))
                    else:
                        msgs.add_ai_message(response_content)

                except Exception as e:
                    st.error(f"An error occurred while processing your request: {e}")
                    msgs.add_ai_message(AIMessage(content=f"I apologize, an error occurred: {e}. Please try again."))

