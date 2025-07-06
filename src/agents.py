# # # src/agents.py
# # from langchain import hub
# # from langchain.agents import create_react_agent, AgentExecutor
# # from langchain_core.prompts import PromptTemplate
# # from langchain_community.chat_message_histories import StreamlitChatMessageHistory
# # from src.llm_utils import get_llm_client
# # from src.tools import get_technical_recommendation, get_stock_price

# # class LangchainStockAgent:
# #     def __init__(self, provider: str, api_key: str):
# #         self.provider = provider
# #         self.api_key = api_key
# #         self.llm = get_llm_client(provider, api_key)
# #         if not self.llm:
# #             raise ValueError(f"Failed to initialize LLM for provider: {provider}")

# #         # The specialized tool list
# #         self.tools = [get_technical_recommendation, get_stock_price]

# #         # Get the standard ReAct prompt from the LangChain Hub
# #         # This prompt is designed to be highly compatible with many models.
# #         prompt = hub.pull("hwchase17/react")
        
# #         # Create the ReAct Agent
# #         agent = create_react_agent(self.llm, self.tools, prompt)
        
# #         self.msgs = StreamlitChatMessageHistory(key="stock_chat_messages")
        
# #         self.agent_executor = AgentExecutor(
# #             agent=agent,
# #             tools=self.tools,
# #             verbose=True,
# #             handle_parsing_errors=True,
# #         )

# #     async def run_agent_with_history(self, user_query: str):
# #         """Runs the ReAct agent."""
# #         return await self.agent_executor.ainvoke(
# #             {
# #                 "input": user_query,
# #                 "chat_history": self.msgs.messages
# #             },
# #         )


# # src/agents.py
# # src/agents.py
# from langchain import hub
# from langchain.agents import create_react_agent, AgentExecutor
# from langchain_community.chat_message_histories import StreamlitChatMessageHistory
# from src.llm_utils import get_llm_client
# from src.tools import get_technical_recommendation, get_fundamental_analysis

# class LangchainStockAgent:
#     def __init__(self, provider: str, api_key: str):
#         self.provider = provider
#         self.api_key = api_key
#         self.llm = get_llm_client(provider, api_key)
#         if not self.llm:
#             raise ValueError(f"Failed to initialize LLM for provider: {provider}")

#         # Final tool list, sector analysis is removed.
#         self.tools = [get_technical_recommendation, get_fundamental_analysis]

#         prompt = hub.pull("hwchase17/react")
        
#         agent = create_react_agent(self.llm, self.tools, prompt)
        
#         self.msgs = StreamlitChatMessageHistory(key="stock_chat_messages")
        
#         self.agent_executor = AgentExecutor(
#             agent=agent,
#             tools=self.tools,
#             verbose=True,
#             handle_parsing_errors=True,
#         )

#     async def run_agent_with_history(self, user_query: str):
#         """Runs the ReAct agent."""
#         return await self.agent_executor.ainvoke(
#             {
#                 "input": user_query,
#                 "chat_history": self.msgs.messages
#             },
#         )


# src/agents.py - DEFINITIVE FINAL VERSION
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from src.llm_utils import get_llm_client
from src.tools import get_technical_recommendation, get_fundamental_analysis, get_latest_news_for_summary

class LangchainStockAgent:
    def __init__(self, provider: str, api_key: str):
        self.provider = provider
        self.api_key = api_key
        self.llm = get_llm_client(provider, api_key)
        if not self.llm: raise ValueError(f"Failed to initialize LLM for provider: {provider}")

        # The final, complete tool list
        self.tools = [get_technical_recommendation, get_fundamental_analysis, get_latest_news_for_summary]
        
        prompt = hub.pull("hwchase17/react")
        
        agent = create_react_agent(self.llm, self.tools, prompt)
        
        self.msgs = StreamlitChatMessageHistory(key="stock_chat_messages")
        
        self.agent_executor = AgentExecutor(
            agent=agent, tools=self.tools, verbose=True, handle_parsing_errors=True
        )

    async def run_agent_with_history(self, user_query: str):
        """Runs the ReAct agent."""
        return await self.agent_executor.ainvoke(
            {"input": user_query, "chat_history": self.msgs.messages},
        )
