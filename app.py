import streamlit as st
import asyncio # Required for async functions
from src.stock_analysis_logic import show_stocks_chatbot
from src.sip_planning_logic import show_sip_planner
from langchain_community.chat_message_histories import StreamlitChatMessageHistory # For persistent chat history
from langchain_core.messages import HumanMessage, AIMessage

# --- Streamlit Page Functions ---

def set_page(page_name):
    """Sets the current page in Streamlit's session state."""
    st.session_state.current_page = page_name

def show_intro_page():
    """Displays the introductory page of the application."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    body {
        font-family: 'Inter', sans-serif;
    }
    .intro-container {
        display: flex;
        flex-direction: column;
        justify-content: center; /* Center vertically */
        align-items: center; /* Center horizontally */
        min-height: 6vh; /* Full viewport height */
        background: linear-gradient(135deg, #6DD5ED 0%, #2193B0 100%); /* Blue gradient */
        color: white;
        text-align: center;
        padding: 20px; /* Padding around content */
        font-family: 'Inter', sans-serif;
    }
    .intro-title {
        font-size: 3.5em;
        font-weight: bold;
        margin-bottom: 0.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .intro-tagline {
        font-size: 1.5em;
        margin-bottom: 2em; /* Space between tagline and button */
        max-width: 800px;
        line-height: 1.6;
    }
    /* Specific styling for the Streamlit button that acts as "Get Started" */
    div.stButton > button:first-child {
        background-color: #FF6B6B; /* Reddish button */
        color: white;
        border-radius: 25px;
        padding: 10px 30px;
        font-size: 1.2em;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        cursor: pointer;
        margin-top: 20px; /* Space above button after tagline */
        margin-bottom: 50px; /* Space below button, before cards */
    }
    div.stButton > button:first-child:hover {
        background-color: #FF4A4A;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.3);
    }

    /* Styles for the new feature highlight cards */
    .feature-card-wrapper { /* Wrapper to control max-width of columns */
        display: flex;
        flex-direction: column; /* Stack columns within this wrapper */
        align-items: center;
        width: 100%;
    }
    .feature-card-row {
        display: flex;
        flex-wrap: wrap; /* Allow cards to wrap to next line on smaller screens */
        justify-content: center;
        gap: 20px; /* Space between cards */
        width: 100%; /* Take full width of its parent (column) */
        max-width: 900px; /* Max width for cards section */
    }
    .feature-card {
        background-color: rgba(255, 255, 255, 0.15); /* Subtle transparent background */
        border-radius: 15px;
        padding: 25px;
        flex: 1; /* Allow cards to grow and shrink */
        min-width: 280px; /* Minimum width before wrapping */
        max-width: 350px; /* Maximum width for individual card */
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        backdrop-filter: blur(5px); /* Slightly blur background for a modern look */
        border: 1px solid rgba(255, 255, 255, 0.3); /* Light border */
    }
    .feature-card:hover {
        transform: translateY(-8px); /* Lift effect on hover */
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    .feature-card h4 {
        font-size: 1.4em;
        color: #FFD700; /* Gold heading */
        margin-bottom: 10px;
        font-weight: bold;
    }
    .feature-card p {
        font-size: 1em;
        line-height: 1.5;
        color: #f0f0f0; /* Light text for description */
        margin-bottom: 15px;
    }
    .feature-card .icon {
        font-size: 2.5em;
        margin-bottom: 15px;
        color: white; /* White icon */
    }
    </style>
    """, unsafe_allow_html=True)

    # Main intro container for title and tagline
    st.markdown("""
    <div class="intro-container">
        <h1 class="intro-title">Your Personal Financial Navigator</h1>
        <p class="intro-tagline">Intelligent insights for smarter investment and planning decisions. Empowering your financial future.</p>
    </div>
    """, unsafe_allow_html=True)

    # Use Streamlit's native button for reliable click handling
    st.button("Get Started", on_click=lambda: set_page("login"))

    # Feature cards container - using st.columns for layout within the Streamlit app
    st.markdown('<div class="feature-card-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="feature-card-row">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3) # Create three columns for the cards

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🤖</div>
            <h4>AI-Powered Stock Analysis</h4>
            <p>Get instant insights on stocks with our intelligent chatbot. Ask about fundamentals, predictions, and more!</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">💰</div>
            <h4>Personalized SIP Plans</h4>
            <p>Receive tailored Systematic Investment Plan recommendations based on your unique financial goals and risk appetite.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">✨</div>
            <h4>Multi-LLM Flexibility</h4>
            <p>Choose your preferred AI powerhouse: Gemini, OpenAI, Groq, HuggingFace, or Cohere for diverse insights.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # Close feature-card-row
    st.markdown('</div>', unsafe_allow_html=True) # Close feature-card-wrapper

def show_login_page():
    """Displays the login page for API key input."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    body {
        font-family: 'Inter', sans-serif;
    }
    .login-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 50vh;
        background: #f0f2f6; /* Light grey background */
        font-family: 'Inter', sans-serif;
    }
    .login-box {
        background: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
        width: 100%;
        max-width: 450px;
        box-sizing: border-box;
    }
    .login-title {
        font-size: 2em;
        font-weight: bold;
        margin-bottom: 1.5em;
        color: #333;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #ccc;
        padding: 12px;
        width: 100%;
        box-sizing: border-box;
    }
    .stRadio>label {
        font-weight: bold;
        margin-right: 15px;
    }
    .stRadio>div {
        justify-content: center;
        margin-bottom: 20px;
        display: flex;
        flex-wrap: wrap; /* Allow radio buttons to wrap */
        gap: 10px; /* Space between radio buttons */
    }
    .stRadio div[role="radio"] { /* Target individual radio buttons */
        background-color: #e9e9e9;
        padding: 8px 15px;
        border-radius: 20px;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }
    .stRadio div[role="radio"]:hover {
        background-color: #dcdcdc;
    }
    .stRadio div[aria-selected="true"] { /* Style for selected radio button */
        background-color: #4CAF50;
        color: white;
    }
    .stButton>button {
        background-color: #4CAF50; /* Green button */
        color: white;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 1.1em;
        border: none;
        box-shadow: 0 3px 5px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    </style>
    <div class="login-container">
        <div class="login-box">
            <h2 class="login-title">Access Your Financial Dashboard</h2>
    """, unsafe_allow_html=True)

    # API key input field
    # Check st.secrets first if deployed, otherwise use session state
    # For local testing, user inputs directly.
    # When deployed, can fetch from secrets: st.secrets.get("OPENAI_API_KEY")
    api_key_input = st.text_input("Enter Your LLM API Key", type="password",
                                   value=st.session_state.get("api_key", ""))
    # LLM provider selection
    llm_provider = st.radio(
        "Select LLM Provider",
        ("Gemini", "OpenAI", "Groq", "HuggingFace", "Cohere"),
        index=("Gemini", "OpenAI", "Groq", "HuggingFace", "Cohere").index(st.session_state.get("llm_provider", "Gemini")),
        horizontal=True
    )

    if st.button("Proceed"):
        if api_key_input:
            st.session_state.api_key = api_key_input
            st.session_state.llm_provider = llm_provider
            st.session_state.logged_in = True
            set_page("main")
            st.rerun() # Rerun to switch to the main page
        else:
            st.warning("Please enter an API key to proceed.")
    st.markdown("</div></div>", unsafe_allow_html=True)



def show_main_app():
    """Displays the main application dashboard with tabs for Stocks and SIP Plan."""
 # Ensure selected_tab is initialized
    if "selected_tab" not in st.session_state:
        st.session_state.selected_tab = "Stocks"
 

# Custom CSS for layout and styling
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    body {
        font-family: 'Inter', sans-serif;
    }
    /* General header styling for the entire row of logo and buttons */
    /* Target the main container that Streamlit wraps columns in */
    div[data-testid="stVerticalBlock"] > div:first-child > div[data-testid="stHorizontalBlock"] {
        background-color: #FFFFFF; /* White header background */
        color: #333; /* Dark text for header */
        border-radius: 10px;
        padding: 10px 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
        align-items: center; /* Vertically center items in this block */
    }

    /* Logo styling */
    h1 { /* Targeting Streamlit's default h1 for st.markdown with bold text */
        font-size: 8em;
        font-weight: bold;
        color: #333333;
        margin: 0; /* Remove default margin */
        padding: 0; /* Remo1.ve default padding */
        display: flex; /* Make it a flex container to align content */
        align-items: center; /* Vertically center text and emoji */
        gap: 10px; /* Space between emoji and text */
        flex-shrink: 0; /* Prevent logo from shrinking */
    }

    /* Style for the actual <button> element within Streamlit's wrapper */
    .stButton > button {
        border-radius: 4px; /* Rectangular look */
        padding: 8px 18px;
        font-weight: bold;
        border: 1px solid #ccc; /* Subtle border */
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        transition: all 0.2s ease;
        cursor: pointer;
        width: auto; /* Allow buttons to size based on content */
        line-height: normal; /* Ensure text sits correctly */
        flex-shrink: 0; /* Prevent buttons from shrinking */
        margin: 0 !important; /* Remove any default margins that push buttons apart */
        display: inline-flex !important; /* Make buttons display inline-flex for side-by-side */
        align-items: center; /* Center text vertically within the button */
        justify-content: center; /* Center text horizontally within the button */
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 3px 6px rgba(0,0,0,0.3);
    }
    /* Active tab style (for primary type button) */
    .stButton > button[data-testid*="stButton-primary"] {
        background-color: #28a745; /* Green for active Stocks */
        color: white;
        border-color: #28a745; /* Match border to background */
    }
    /* Inactive tab style (for secondary type button) */
    .stButton > button[data-testid*="stButton-secondary"] {
        background-color: #ffc107; /* Yellow for inactive SIP or vice-versa */
        color: #333;
        border-color: #ffc107; /* Match border to background */
    }

    /* Adjust spacing and alignment within the columns for buttons */
    div[data-testid="stColumn"] {
        display: flex; /* Make columns flex containers */
        align-items: center; /* Vertically center content */
        padding: 0 !important; /* Remove all default padding from columns */
        margin: 0 !important; /* Remove all default margin from columns */
        gap: 10px; /* Explicit gap between button columns */
    }
    /* For the column that contains the buttons, align them to the end (right) */
    div[data-testid="stColumn"]:nth-child(2) {
        justify-content: flex-end; /* Align contents of this column to the right */
        flex-grow: 1; /* Allow this column to take up remaining space */
    }
    /* For the button columns themselves (within the button-containing column) */
    div[data-testid="stColumn"]:nth-child(2) > div[data-testid="stVerticalBlock"] > div > div[data-testid^="stColumn"] {
        flex-grow: 0; /* Prevent individual button columns from growing too much */
        flex-shrink: 0; /* Prevent them from shrinking */
        width: auto; /* Allow buttons to dictate their column width */
    }
    /* Remove padding between the button columns if they were separated by default */
    div[data-testid="stColumn"]:nth-child(2) > div[data-testid="stVerticalBlock"] > div > div[data-testid^="stColumn"]:first-child {
        padding-right: 5px !important; /* Small gap between buttons */
    }
    div[data-testid="stColumn"]:nth-child(2) > div[data-testid="stVerticalBlock"] > div > div[data-testid^="stColumn"]:nth-child(2) {
        padding-left: 5px !important; /* Small gap between buttons */
    }


    /* Chat message styling (general app styles) */
    .stChatMessage {
        background-color: #f8f9fa; /* Light background for chat area */
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    /* Style for user messages */
    .stChatMessage[data-testid="chat-message-container"]:nth-child(odd) { /* Odd children for user, assuming user is first */
        background-color: #e6f7ff; /* Light blue */
        align-self: flex-end;
        margin-left: auto;
        text-align: right;
    }
    /* Style for assistant messages */
    .stChatMessage[data-testid="chat-message-container"]:nth-child(even) { /* Even children for assistant */
        background-color: #f0f0f0; /* Light gray */
        align-self: flex-start;
        margin-right: auto;
        text-align: left;
    }
    /* Ensure chat input stays at the bottom */
    .stChatInput {
        position: sticky;
        bottom: 0;
        background-color: white;
        padding: 10px 0;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

    # Main header structure using Streamlit columns
    # col_logo for the logo, col_buttons_wrapper to contain the two buttons,
    # and col_spacer to absorb remaining space (not needed if col_buttons_wrapper grows)
    col_logo, col_buttons_wrapper = st.columns([0.6, 0.4]) # Adjust proportions as needed

    with col_logo:
       #st.markdown('<div class="app-logo">📈 Financial Navigator</div>', unsafe_allow_html=True)
       st.markdown('<div class="app-logo" style="font-weight: bold; font-size: 30px;">📈 Financial Navigator</div>', unsafe_allow_html=True)

        # Streamlit renders st.markdown with bold as h1

    with col_buttons_wrapper:
        # Inner columns to strictly position the two buttons side-by-side
        # Use very small, equal ratios, or just one wide column if justify-content works well.
        # Let's try to put them directly in this column and rely on flexbox within it.
        btn_col_stocks, btn_col_sip = st.columns([1, 1]) # These are columns *within* col_buttons_wrapper

        with btn_col_stocks:
            if st.button('Stocks', key='stocks_tab_button', type='primary' if st.session_state.selected_tab == 'Stocks' else 'secondary'):
                st.session_state.selected_tab = 'Stocks'
                st.rerun() # Force rerun for immediate tab change

        with btn_col_sip:
            if st.button('SIP Plan', key='sip_tab_button', type='primary' if st.session_state.selected_tab == 'SIP' else 'secondary'):
                st.session_state.selected_tab = 'SIP'
                st.rerun() # Force rerun for immediate tab change

    st.markdown("---") # Visual separator below the header

    # Conditional rendering of content based on selected tab in session state
    if st.session_state.selected_tab == "Stocks":
        asyncio.run(show_stocks_chatbot())
    elif st.session_state.selected_tab == "SIP":
        asyncio.run(show_sip_planner())


        
# --- Main App Logic (Routing) ---

# Initialize session state variables if they don't exist
if "current_page" not in st.session_state:
    st.session_state.current_page = "intro"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "api_key" not in st.session_state:
    st.session_state.api_key = "" # Will be populated from UI input
if "llm_provider" not in st.session_state:
    st.session_state.llm_provider = "Gemini" # Default provider for first load
if "selected_tab" not in st.session_state:
    st.session_state.selected_tab = "Stocks" # Default tab for main page


# Set Streamlit page configuration (must be called once at the top)
st.set_page_config(page_title="Financial Navigator", layout="wide", initial_sidebar_state="collapsed")


# Routing logic based on session state
if st.session_state.current_page == "intro":
    show_intro_page()
elif st.session_state.current_page == "login":
    show_login_page()
elif st.session_state.current_page == "main" and st.session_state.logged_in:
    show_main_app()
else:
    # Fallback: if not logged in or unexpected state, go to intro page
    st.session_state.current_page = "intro"
    st.rerun() # Rerun to apply the page change

