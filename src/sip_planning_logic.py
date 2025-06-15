import streamlit as st
import json
from src.llm_utils import call_llm_api_direct # Use direct LLM call for this
from src.tools import google_search_tool # Use google_search_tool for initial context
from langchain_core.messages import HumanMessage # For direct LLM call history formatting

async def show_sip_planner():
    """
    Manages the Streamlit UI and logic for the SIP plan recommendations.
    """
    st.subheader("💰 SIP Plan Recommendations")

    st.markdown("Enter your preferences to get a personalized (simulated) SIP plan recommendation.")

    # Get API key and provider from session state
    current_api_key = st.session_state.get("api_key", "")
    current_llm_provider = st.session_state.get("llm_provider", "Gemini")

    if not current_api_key:
        st.warning("Please enter your API key on the login page to generate SIP plans.")
        return

    investment_goal = st.selectbox("What is your investment goal?",
                                  ["Retirement", "Child's Education", "Buying a House", "Wealth Creation", "Other"])
    risk_appetite = st.radio("What is your risk appetite?",
                             ["Low (Capital Preservation)", "Medium (Balanced Growth)", "High (Aggressive Growth)"])
    investment_horizon = st.slider("What is your investment horizon (in years)?", 1, 30, 10)
    monthly_investment = st.number_input("What is your monthly investment amount (in INR)?", min_value=500, value=5000, step=500)

    if st.button("Generate SIP Plan"):
        with st.spinner(f"Generating SIP plan with {current_llm_provider}..."):
            # Simulate initial search for context for the LLM
            search_query_context = f"best SIP plans for {investment_goal} with {risk_appetite} risk and {investment_horizon} years horizon"
            simulated_search_results = google_search_tool(search_query_context)

            # Prepare the prompt for the LLM
            llm_prompt = f"""
            You are a helpful financial planning AI assistant specializing in SIPs.
            Based on the user's preferences and the following simulated general knowledge/search results,
            recommend suitable SIP (Systematic Investment Plan) categories.
            For each recommendation, explain why it is suitable, suggest a realistic investment duration,
            and categorize its risk level.

            User Preferences:
            Goal: {investment_goal}
            Risk Appetite: {risk_appetite}
            Investment Horizon: {investment_horizon} years
            Monthly Investment: INR {monthly_investment}

            Simulated General Knowledge/Search Results for SIP planning:
            {simulated_search_results}

            Provide your response in a structured JSON format, including a list of recommendations.
            After the JSON, also include a short, conversational summary and the mandatory disclaimer.

            JSON Schema for recommendations:
            ```json
            [
              {{
                "name": "string",
                "reasoning": "string",
                "duration": "string",
                "risk_level": "string"
              }}
            ]
            ```
            Ensure the JSON is well-formed and complete.
            """

            # Define the JSON schema for the response (for LLM to try and adhere to)
            # This is more of a guideline for the LLM for most providers when not using structured_output.
            sip_response_schema = {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "name": {"type": "STRING", "description": "Name of the SIP fund category"},
                        "reasoning": {"type": "STRING", "description": "Why this SIP is suitable"},
                        "duration": {"type": "STRING", "description": "Suggested investment duration"},
                        "risk_level": {"type": "STRING", "description": "Risk level of the fund (e.g., 'Low', 'Medium', 'High', 'Medium-High')"}
                    },
                    "required": ["name", "reasoning", "duration", "risk_level"]
                }
            }

            # Call the LLM API based on selected provider using the direct call utility
            raw_response = await call_llm_api_direct(
                llm_prompt, chat_history=[], provider=current_llm_provider, api_key=current_api_key,
                is_json_response=True, response_schema=sip_response_schema # Pass schema, though direct LLM call might just use it for prompting
            )

            if raw_response is None:
                st.error("Failed to get a response from the AI. Please check your API key or try again.")
                return

            try:
                # Attempt to parse JSON and extract conversational part
                json_start = raw_response.find("[")
                json_end = raw_response.rfind("]")

                recommendations = []
                conversational_summary = ""

                if json_start != -1 and json_end != -1:
                    json_str = raw_response[json_start : json_end + 1]
                    recommendations = json.loads(json_str)
                    conversational_summary = raw_response[json_end + 1:].strip()
                else:
                    # If JSON parsing fails, treat the whole response as text
                    st.warning("Could not parse structured recommendations. Displaying raw AI response.")
                    st.write(raw_response)
                    return

                if recommendations:
                    st.success("Here's a simulated SIP plan tailored to your preferences:")
                    for rec in recommendations:
                        st.markdown(f"##### 🚀 {rec.get('name', 'N/A')}")
                        st.write(f"**💡 Reasoning:** {rec.get('reasoning', 'N/A')}")
                        st.write(f"**⏳ Suggested Duration:** {rec.get('duration', 'N/A')}")
                        st.write(f"**⚠️ Risk Level:** {rec.get('risk_level', 'N/A')}")
                        st.markdown("---")

                    if conversational_summary:
                        st.info(conversational_summary)
                else:
                    st.info("The AI did not provide specific SIP recommendations based on your input. Please try adjusting your preferences or ask a more specific query.")

            except json.JSONDecodeError as e:
                st.error(f"Failed to decode JSON from AI response: {e}. Raw response: {raw_response}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

            st.caption("Disclaimer: This information is for educational purposes only and not financial advice. Please consult a qualified financial advisor before making any investment decisions.")

