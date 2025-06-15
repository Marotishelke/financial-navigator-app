from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_huggingface.chat_models import ChatHuggingFace # For chat models
from langchain_cohere.chat_models import ChatCohere
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
import streamlit as st

def get_llm_client(provider: str, api_key: str):
    """
    Initializes and returns a LangChain LLM client based on the provider.
    """
    if not api_key:
        st.error(f"API key for {provider} is missing. Please provide it on the login page.")
        return None

    try:
        if provider == "Gemini":
            # For Canvas, key might be provided automatically, but for local consistency, use the input.
            return ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key, temperature=0.7, convert_system_message_to_human=True)
        elif provider == "OpenAI":
            return ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key, temperature=0.7)
        elif provider == "Groq":
            return ChatGroq(model="llama3-8b-8192", groq_api_key=api_key, temperature=0.7) # Or other Groq models like "llama3-70b-8192"
        elif provider == "HuggingFace":
            # HuggingFace requires a specific endpoint and model.
            # This is a generic example using a common HF chat model.
            # You might need to adjust `model_id` for specific tasks.
            # `HuggingFaceEndpoint` or `HuggingFacePipeline` might be needed for more complex cases.
            # Using ChatHuggingFace which uses the HuggingFace Inference API with a specified model.
            # Ensure the model_id corresponds to a chat-compatible model on HF Hub.
            return ChatHuggingFace(
                llm=None, # Not using direct LLM, but a model from HF Inference API
                model_id="HuggingFaceH4/zephyr-7b-beta", # Example chat model, choose one that supports chat
                huggingfacehub_api_token=api_key,
                temperature=0.7
            )
        elif provider == "Cohere":
            return ChatCohere(model="command-r", cohere_api_key=api_key, temperature=0.7) # Or 'command-r-plus'
        else:
            st.error(f"Unsupported LLM provider: {provider}")
            return None
    except Exception as e:
        st.error(f"Error initializing {provider} LLM: {e}")
        return None

def format_messages_for_langchain(chat_history: list) -> list[BaseMessage]:
    """
    Converts a custom chat history format to LangChain's BaseMessage format.
    """
    langchain_messages = []
    for msg in chat_history:
        if msg["role"] == "user":
            langchain_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            langchain_messages.append(AIMessage(content=msg["content"]))
        # Add other roles if necessary, e.g., SystemMessage
    return langchain_messages

# This function might not be directly used if AgentExecutor handles chat history
# but is kept for SIP planning logic which uses direct LLM calls.
async def call_llm_api_direct(prompt: str, chat_history: list, provider: str, api_key: str, is_json_response: bool = False, response_schema: dict = None):
    """
    Directly calls an LLM via LangChain client. Used for non-agentic flows (like SIP).
    """
    llm = get_llm_client(provider, api_key)
    if not llm:
        return None

    messages = format_messages_for_langchain(chat_history)
    messages.append(HumanMessage(content=prompt))

    try:
        # For JSON responses, we primarily rely on prompt engineering for most models
        # and on specific features if the LLM/LangChain integration supports it.
        if is_json_response and provider == "Gemini":
            # Gemini-specific way to request JSON output if schema is provided
            # This requires a model that supports structured responses.
            # The ChatGoogleGenerativeAI class doesn't directly expose response_schema
            # in its invoke, so prompt engineering is usually relied upon.
            # A more robust solution might use `with_structured_output` if available and model supports.
            # For simplicity, we'll continue with prompt engineering for JSON and manual parsing.
            pass

        response = await llm.ainvoke(messages)
        return response.content
    except Exception as e:
        st.error(f"Error calling LLM directly: {e}")
        return None

