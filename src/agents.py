import json
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_community.chat_message_histories import StreamlitChatMessageHistory # For persistent chat history
import streamlit as st

from src.llm_utils import get_llm_client # Import the LLM client initializer
from src.tools import google_search_tool, stock_data_fetcher_tool, chart_generator_tool # Import decorated tools

class LangchainStockAgent:
    def __init__(self, provider: str, api_key: str):
        self.provider = provider
        self.api_key = api_key
        self.llm = get_llm_client(provider, api_key)
        if not self.llm:
            raise ValueError(f"Failed to initialize LLM for provider: {provider}")

        # Define the tools available to the agent
        self.tools = [google_search_tool, stock_data_fetcher_tool]

        # Define the prompt template for the agent
        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""
                    You are a helpful financial AI assistant. Your goal is to help users with stock analysis.
                    You have access to tools to gather information.
                    If the user asks for fundamental analysis, prediction, buy/sell/hold recommendation,
                    or sector analysis, use the `google_search_tool`.
                    If the user asks for a stock chart or historical data, use the `stock_data_fetcher_tool`.
                    Always be polite and provide clear, concise answers.
                    After providing information, always include the disclaimer:
                    "Disclaimer: This information is for educational purposes only and not financial advice.
                    Please consult a qualified financial advisor before making any investment decisions."
                    """
                ),
                MessagesPlaceholder(variable_name="chat_history"), # For conversational memory
                HumanMessage(content="{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"), # For agent's internal thought process
            ]
        )

        # Create the LangChain agent
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)

        # Create the AgentExecutor
        # StreamlitChatMessageHistory integrates directly with st.session_state
        self.msgs = StreamlitChatMessageHistory(key="stock_chat_messages")
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True, # Set to True to see agent's thought process in console
            handle_parsing_errors=True,
            # Pass chat history to the agent executor for conversational memory
            # The 'history' variable in the prompt is mapped to self.msgs.messages
            # and the 'input' is the current prompt.
            # This is handled by `RunnableWithMessageHistory` or by passing messages directly.
        )

    async def run_agent_with_history(self, user_query: str):
        """
        Runs the LangChain agent with conversation history.
        The LangChain AgentExecutor manages the thought process and tool calling.
        """
        # Prepare the input for the agent executor
        # AgentExecutor expects 'input' for the current query and 'chat_history' for memory.
        # We'll pass the StreamlitChatMessageHistory directly to the prompt.
        try:
            # We use `ainvoke` for async execution
            response = await self.agent_executor.ainvoke(
                {
                    "input": user_query,
                    "chat_history": self.msgs.messages # Pass the entire history
                },
                # Streamlit callback to show agent thinking process if verbose=True
                # Note: StreamlitCallbackHandler is mostly for older agent types or specific needs.
                # For basic agent outputs, just printing to console for verbose=True is often enough.
                # {"callbacks": [StreamlitCallbackHandler(st.container())]} # Uncomment for callback visualization
            )
            # The output of AgentExecutor is usually a dictionary with an 'output' key
            return response.get("output", "No response generated."), {} # Return output and empty metadata for now.
        except Exception as e:
            return f"An error occurred while the AI was processing: {e}", {}

