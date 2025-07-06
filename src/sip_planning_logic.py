# import streamlit as st
# import json
# from src.llm_utils import call_llm_api_direct # Use direct LLM call for this
# # Removed: from src.tools import google_search_tool # No longer using for explicit SIP context

# async def show_sip_planner():
#     """
#     Manages the Streamlit UI and logic for the SIP plan recommendations.
#     The LLM dynamically generates recommendations based on user inputs.
#     """
#     st.subheader("💰 SIP Plan Recommendations")

#     st.markdown("Tell me your financial goal and preferences, and I'll recommend a personalized SIP strategy.")

#     # Get API key and provider from session state
#     current_api_key = st.session_state.get("api_key", "")
#     current_llm_provider = st.session_state.get("llm_provider", "Gemini")

#     if not current_api_key:
#         st.warning("Please enter your API key on the login page to generate SIP plans.")
#         return

#     investment_goal = st.selectbox("What is your investment goal?",
#                                   ["Retirement", "Child's Education", "Buying a House", "Wealth Creation", "Other"])
#     risk_appetite = st.radio("What is your risk appetite?",
#                              ["Low (Capital Preservation)", "Medium (Balanced Growth)", "High (Aggressive Growth)"])
#     investment_horizon = st.slider("What is your investment horizon (in years)?", 1, 30, 10)
#     monthly_investment = st.number_input("What is your monthly investment amount (in INR)?", min_value=500, value=5000, step=500)

#     if st.button("Generate SIP Plan"):
#         with st.spinner(f"Crafting your SIP plan with {current_llm_provider}..."):
#             # Prepare the prompt for the LLM. It directly asks the LLM to generate the plan
#             # based on its general financial knowledge and the user's inputs.
#             llm_prompt = f"""
#             You are a friendly and easy-to-understand financial advisor specializing in Systematic Investment Plans (SIPs).
#             Based on the following user preferences, provide a personalized SIP recommendation.

#             Explain your recommendations in simple, clear, and encouraging language.
#             First, give a short, conversational summary of the plan.
#             Then, provide structured recommendations in a JSON array.

#             User Preferences:
#             - Goal: {investment_goal}
#             - Risk Appetite: {risk_appetite}
#             - Investment Horizon: {investment_horizon} years
#             - Monthly Investment: INR {monthly_investment}

#             Recommendations should cover:
#             - **Fund Category/Type:** (e.g., Equity Large Cap, Balanced Advantage, Debt Short Duration)
#             - **Why it's Suitable:** Explain simply how it aligns with the user's preferences.
#             - **Expected Risk Level:** (e.g., Low, Moderate, High)
#             - **Key Considerations:** Any important points for the user (e.g., long-term commitment, market volatility).

#             JSON Schema for recommendations (as an array of objects):
#             ```json
#             [
#               {{
#                 "fund_category": "string",
#                 "suitability_reason": "string",
#                 "expected_risk": "string",
#                 "key_considerations": "string"
#               }}
#             ]
#             ```
#             Ensure the JSON is well-formed and complete, and then follow it with your conversational summary and the mandatory disclaimer.
#             """

#             # No specific response_schema for direct LLM call unless the LLM API explicitly supports it.
#             # We'll rely on prompt engineering for JSON output and robust parsing.
#             raw_response = await call_llm_api_direct(
#                 llm_prompt, chat_history=[], provider=current_llm_provider, api_key=current_api_key
#             )

#             if raw_response is None:
#                 st.error("Failed to get a response from the AI. Please check your API key or try again.")
#                 return

#             try:
#                 # Attempt to parse JSON and extract conversational part
#                 json_start = raw_response.find("[")
#                 json_end = raw_response.rfind("]")

#                 recommendations = []
#                 conversational_summary_text = ""

#                 if json_start != -1 and json_end != -1:
#                     json_str = raw_response[json_start : json_end + 1]
#                     try:
#                         recommendations = json.loads(json_str)
#                         conversational_summary_text = raw_response[json_end + 1:].strip()
#                     except json.JSONDecodeError:
#                         st.warning("AI response contained JSON but it was malformed. Displaying full raw AI response.")
#                         st.write(raw_response)
#                         return
#                 else:
#                     # If no JSON or malformed, treat the whole response as a conversational summary
#                     st.info("The AI generated a conversational response for your SIP plan. Here it is:")
#                     st.markdown(raw_response) # Display the whole response as markdown
#                     st.caption("Disclaimer: This information is for educational purposes only and not financial advice. Please consult a qualified financial advisor before making any investment decisions.")
#                     return

#                 if recommendations:
#                     st.success("Here's a personalized SIP plan tailored to your preferences:")
#                     if conversational_summary_text:
#                         st.info(conversational_summary_text) # Display the initial conversational summary

#                     for i, rec in enumerate(recommendations):
#                         st.markdown(f"#### 💡 Recommendation {i+1}: {rec.get('fund_category', 'N/A')}")
#                         st.markdown(f"**Why it's Suitable:** {rec.get('suitability_reason', 'N/A')}")
#                         st.markdown(f"**Expected Risk:** {rec.get('expected_risk', 'N/A')}")
#                         st.markdown(f"**Key Considerations:** {rec.get('key_considerations', 'N/A')}")
#                         if i < len(recommendations) - 1:
#                             st.markdown("---") # Separator between recommendations
                    
#                     st.markdown("---") # Final separator
#                 else:
#                     st.info("The AI did not provide specific structured SIP recommendations based on your input. Please try adjusting your preferences or ask a more specific query.")

#             except Exception as e:
#                 st.error(f"An unexpected error occurred while processing the AI response: {e}")

#             st.caption("Disclaimer: This information is for educational purposes only and not financial advice. Please consult a qualified financial advisor before making any investment decisions.")


# # src/sip_planning_logic.py
# import streamlit as st
# import json
# from src.llm_utils import call_llm_api_direct

# def calculate_sip_future_value(monthly_investment, annual_rate, years):
#     """Calculates the future value of a Systematic Investment Plan."""
#     if annual_rate <= 0:
#         return monthly_investment * 12 * years
#     monthly_rate = (annual_rate / 100) / 12
#     months = years * 12
#     future_value = monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
#     return future_value

# async def show_sip_planner():
#     """
#     Manages the Streamlit UI and logic for the SIP plan recommendations.
#     This version features an enhanced UI and suggests specific fund examples.
#     """
#     st.subheader("💰 SIP Plan & Future Value Calculator")
#     st.markdown("Define your goal, and I'll recommend a personalized SIP strategy and project your potential wealth.")

#     # --- Custom CSS for a more attractive UI ---
#     st.markdown("""
#     <style>
#     /* Main container for inputs */
#     .input-container {
#         background-color: #f8f9fa;
#         border-radius: 10px;
#         padding: 25px;
#         box-shadow: 0 4px 8px rgba(0,0,0,0.1);
#         border: 1px solid #e9ecef;
#     }
#     /* Style for recommendation cards */
#     .recommendation-card {
#         background-color: #ffffff;
#         border-radius: 10px;
#         padding: 20px;
#         margin-bottom: 15px;
#         border: 1px solid #dee2e6;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.05);
#     }
#     .recommendation-card h4 {
#         color: #007bff;
#         margin-bottom: 15px;
#         display: flex;
#         align-items: center;
#     }
#     .recommendation-card h4 .icon {
#         margin-right: 10px;
#         font-size: 1.5em;
#     }
#     .fund-example {
#         background-color: #e9f5ff;
#         border-left: 5px solid #007bff;
#         padding: 10px;
#         margin-top: 15px;
#         border-radius: 5px;
#         font-style: italic;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     # --- Input Section with New Layout ---
#     with st.container():
#         st.markdown('<div class="input-container">', unsafe_allow_html=True)
        
#         col1, col2 = st.columns(2)
#         with col1:
#             investment_goal = st.selectbox("Investment Goal", ["Retirement", "Child's Education", "Buying a House", "Wealth Creation", "Other"])
#             risk_appetite = st.radio("Risk Appetite", ["Low (Capital Preservation)", "Medium (Balanced Growth)", "High (Aggressive Growth)"])
        
#         with col2:
#             investment_horizon = st.slider("Investment Horizon (Years)", 1, 40, 10)
#             monthly_investment = st.number_input("Monthly Investment (INR)", min_value=500, value=5000, step=500)

#         expected_return_rate = st.slider(
#             "Expected Annual Return (%)", 1.0, 25.0, 12.0, 0.5,
#             help="Enter the average annual return you expect. 12% is a common long-term average for equity funds, but this can vary."
#         )
        
#         st.markdown('</div>', unsafe_allow_html=True)

#     # --- Button and Output Section ---
#     if st.button("Generate SIP Plan & Calculate Future Value", type="primary"):
#         current_api_key = st.session_state.get("api_key", "")
#         current_llm_provider = st.session_state.get("llm_provider", "Gemini")

#         if not current_api_key:
#             st.warning("Please enter your API key on the login page to generate SIP plans.")
#             return

#         st.markdown("---")
#         projected_corpus = calculate_sip_future_value(monthly_investment, expected_return_rate, investment_horizon)
#         total_invested = monthly_investment * 12 * investment_horizon
#         wealth_gained = projected_corpus - total_invested

#         st.success(f"**Investment Growth Projection**")
#         metric_col1, metric_col2, metric_col3 = st.columns(3)
#         metric_col1.metric("Projected Corpus", f"₹{projected_corpus:,.0f}")
#         metric_col2.metric("Total Amount Invested", f"₹{total_invested:,.0f}")
#         metric_col3.metric("Estimated Wealth Gained", f"₹{wealth_gained:,.0f}")
#         st.caption(f"Based on investing ₹{monthly_investment:,} per month for {investment_horizon} years with an expected annual return of {expected_return_rate}%.")
#         st.markdown("---")

#         with st.spinner(f"Crafting your personalized plan with {current_llm_provider}..."):
#             llm_prompt = f"""
#             You are a friendly financial advisor. Based on the following user preferences, provide a personalized SIP recommendation.
#             First, give a short, conversational summary.
#             Then, provide structured recommendations in a JSON array. For each recommendation, suggest 1-2 examples of well-known, real Indian mutual funds that fit the category.

#             User Preferences:
#             - Goal: {investment_goal}
#             - Risk Appetite: {risk_appetite}
#             - Investment Horizon: {investment_horizon} years
#             - Monthly Investment: INR {monthly_investment}

#             JSON Schema for recommendations (as an array of objects):
#             ```json
#             [
#               {{
#                 "fund_category": "e.g., Equity Large Cap Fund",
#                 "suitability_reason": "Explain simply why it fits the user profile.",
#                 "expected_risk": "e.g., High",
#                 "fund_examples": [ "Example Fund Name 1 (e.g., Axis Bluechip Fund)", "Example Fund Name 2 (e.g., Mirae Asset Large Cap Fund)" ]
#               }}
#             ]
#             ```
#             Ensure the JSON is well-formed. After the JSON, write your conversational summary and the disclaimer.
#             """

#             raw_response = await call_llm_api_direct(llm_prompt, [], current_llm_provider, current_api_key)

#             if raw_response is None:
#                 st.error("Failed to get a response from the AI.")
#                 return

#             try:
#                 st.info("**AI-Powered Recommendation Strategy**")
                
#                 json_start = raw_response.find('[')
#                 json_end = raw_response.rfind(']') + 1
#                 json_str = raw_response[json_start:json_end]
                
#                 recommendations = json.loads(json_str)
#                 summary_text = raw_response.replace(json_str, "").strip()

#                 st.markdown(summary_text)
#                 st.markdown("---")

#                 for rec in recommendations:
#                     st.markdown(f"""
#                     <div class="recommendation-card">
#                         <h4><span class="icon">💡</span>{rec.get('fund_category', 'N/A')}</h4>
#                         <p><strong>Why it's Suitable:</strong> {rec.get('suitability_reason', 'N/A')}</p>
#                         <p><strong>Expected Risk:</strong> {rec.get('expected_risk', 'N/A')}</p>
#                         <div class="fund-example">
#                             <strong>Fund Examples:</strong>
#                             <ul>
#                                 {"".join(f"<li>{fund}</li>" for fund in rec.get('fund_examples', []))}
#                             </ul>
#                         </div>
#                     </div>
#                     """, unsafe_allow_html=True)

#             except (json.JSONDecodeError, IndexError):
#                 st.warning("Could not parse a structured plan from the AI. Displaying its full response:")
#                 st.markdown(raw_response)
            
#             st.caption("""
#             **Disclaimer:** The fund names mentioned are illustrative examples based on the AI's training data and are not live, personalized financial advice or endorsements. 
#             Mutual fund investments are subject to market risks. Please consult with a qualified financial advisor before making any investment decisions.
#             """)



# src/sip_planning_logic.py - DEFINITIVE FINAL VERSION
import streamlit as st
import json
from src.llm_utils import call_llm_api_direct

def calculate_sip_future_value(monthly_investment, annual_rate, years):
    """Calculates the future value of a Systematic Investment Plan."""
    if annual_rate <= 0: return monthly_investment * 12 * years
    monthly_rate = (annual_rate / 100) / 12
    months = years * 12
    future_value = monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
    return future_value

async def show_sip_planner():
    """
    Manages the Streamlit UI and logic for the SIP plan recommendations.
    This version features an enhanced UI and a multi-phase strategy output.
    """
    st.title("💰 Personalized SIP Strategy Planner")
    st.markdown("Define your goal, and I'll recommend a phased SIP strategy and project your potential wealth.")

    st.markdown("""
    <style>
        .input-container { background-color: #f8f9fa; border-radius: 10px; padding: 25px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border: 1px solid #e9ecef; margin-bottom: 2em; }
        .results-container { margin-top: 2em; }
        .phase-card { background-color: #ffffff; border-radius: 10px; padding: 20px; margin-bottom: 15px; border-left: 5px solid #0d6efd; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .phase-card h4 { color: #0d6efd; margin-bottom: 5px; }
        .phase-card em { color: #6c757d; font-size: 0.9em; }
        .fund-example { background-color: #e9f5ff; border-left: 3px solid #007bff; padding: 10px; margin-top: 15px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

    with st.container(border=False):
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            investment_goal = st.selectbox("Investment Goal", ["Wealth Creation", "Retirement", "Child's Education", "Buying a House", "Other"])
            risk_appetite = st.radio("Risk Appetite", ["High (Aggressive Growth)", "Medium (Balanced Growth)", "Low (Capital Preservation)"])
        with col2:
            investment_horizon = st.slider("Investment Horizon (Years)", 1, 40, 10)
            monthly_investment = st.number_input("Monthly Investment (INR)", min_value=500, value=10000, step=1000)
        expected_return_rate = st.slider("Expected Annual Return (%)", 1.0, 25.0, 12.0, 0.5)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Generate My Investment Plan", type="primary", use_container_width=True):
        current_api_key = st.session_state.get("api_key", "")
        current_llm_provider = st.session_state.get("llm_provider", "Groq")

        if not current_api_key:
            st.warning("Please enter your API key on the login page.")
            return

        with st.container(border=True):
            projected_corpus = calculate_sip_future_value(monthly_investment, expected_return_rate, investment_horizon)
            total_invested = monthly_investment * 12 * investment_horizon
            wealth_gained = projected_corpus - total_invested
            st.subheader("Investment Growth Projection")
            p_col1, p_col2, p_col3 = st.columns(3)
            p_col1.metric("Projected Wealth", f"₹{projected_corpus:,.0f}")
            p_col2.metric("Total Invested", f"₹{total_invested:,.0f}")
            p_col3.metric("Wealth Gained", f"₹{wealth_gained:,.0f}")
            st.caption(f"Based on investing ₹{monthly_investment:,} per month for {investment_horizon} years with an expected annual return of {expected_return_rate}%.")

        with st.spinner(f"Crafting your personalized plan..."):
            llm_prompt = f"""
            You are an expert financial advisor. Based on the user's preferences, create a multi-phase SIP strategy. Your entire output must be a single, well-formed JSON object. Do not add any text before or after the JSON object.

            User Preferences:
            - Goal: {investment_goal}
            - Risk Appetite: {risk_appetite}
            - Investment Horizon: {investment_horizon} years

            JSON Schema:
            {{
              "strategy_summary": "A brief, one-sentence summary of the overall plan.",
              "phases": [
                {{
                  "phase_name": "e.g., Phase 1: Aggressive Growth",
                  "phase_duration": "e.g., Years 1-7",
                  "phase_description": "e.g., Focus on maximizing returns through high-growth equity.",
                  "recommended_funds": [
                    {{
                      "fund_category": "e.g., Equity Flexi Cap Fund",
                      "fund_examples": ["Parag Parikh Flexi Cap Fund", "HDFC Flexi Cap Fund"]
                    }}
                  ]
                }}
              ]
            }}
            """
            raw_response = await call_llm_api_direct(llm_prompt, [], current_llm_provider, current_api_key)

            if raw_response is None:
                st.error("Failed to get a response from the AI.")
                return

            try:
                st.subheader("Your AI-Powered Investment Strategy")
                
                # --- THIS IS THE FIX ---
                # Find the first '{' and the last '}' to correctly extract the JSON object.
                json_start = raw_response.find('{')
                json_end = raw_response.rfind('}') + 1

                if json_start == -1: # If no JSON object is found
                    raise json.JSONDecodeError("No JSON object found in response.", raw_response, 0)
                
                json_str = raw_response[json_start:json_end]
                plan_data = json.loads(json_str)
                
                if plan_data.get("strategy_summary"):
                    st.info(plan_data["strategy_summary"])

                for phase in plan_data.get("phases", []):
                    st.markdown(f"""
                    <div class="phase-card">
                        <h4>{phase.get('phase_name', 'N/A')}</h4>
                        <em>Duration: {phase.get('phase_duration', 'N/A')}</em>
                        <p>{phase.get('phase_description', '')}</p>
                    """, unsafe_allow_html=True)
                    
                    for fund in phase.get("recommended_funds", []):
                        st.markdown(f"""
                        <div class="fund-example">
                            <strong>Recommended Category: {fund.get('fund_category', 'N/A')}</strong>
                            <ul>
                                {"".join(f"<li>{example}</li>" for example in fund.get('fund_examples', []))}
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            except (json.JSONDecodeError, IndexError):
                st.warning("Could not parse a structured plan from the AI. Displaying its full response:")
                st.markdown(raw_response)
            
            st.caption("""
            **Disclaimer:** The fund names mentioned are illustrative examples based on the AI's training data and are not live, personalized financial advice or endorsements. 
            Mutual fund investments are subject to market risks. Please consult with a qualified financial advisor before making any investment decisions.
            """)