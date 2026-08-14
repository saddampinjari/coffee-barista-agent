import os
from dotenv import load_dotenv
load_dotenv(override=True)  # Load and override environment variables from .env file

if not os.getenv("GEMINI_API_KEY") and os.getenv("GOOGLE_API_KEY"):
    os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")

import json
import streamlit as st
from google.genai import types
from google.adk.runners import Runner  
from google.adk.sessions import InMemorySessionService
from agent import get_barista_agent


st.set_page_config(
    page_title="AI Barista", 
    page_icon="☕", 
    layout="wide"
)

# ==========================================
# CUSTOM THEME & HORIZONTAL SLIDER CSS
# ==========================================
custom_css = """
<style>
    /* Hide Streamlit Header, Toolbar, Main Menu & Footer */
    header[data-testid="stHeader"],
    [data-testid="stToolbar"],
    #MainMenu,
    footer {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }

    /* Global background and text color */
    .stApp {
        background-color: #F5F0EB !important;
        color: #231B18 !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }


    /* Menu Header Section */
    .menu-header-container {
        margin-bottom: 20px;
    }

    .menu-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        color: #231B18;
        font-size: 2.2rem;
        letter-spacing: 1.5px;
        margin-bottom: 4px;
        text-transform: uppercase;
    }

    .menu-subtitle {
        color: #7C6E65;
        font-size: 0.95rem;
        max-width: 500px;
        line-height: 1.4;
    }

    /* Horizontal Scroll Wrapper */
    .scroll-container {
        display: flex;
        overflow-x: auto;
        gap: 20px;
        padding-top: 45px;
        padding-bottom: 20px;
        scroll-behavior: smooth;
    }

    .scroll-container::-webkit-scrollbar {
        height: 6px;
    }
    .scroll-container::-webkit-scrollbar-track {
        background: #E5DDD5;
        border-radius: 10px;
    }
    .scroll-container::-webkit-scrollbar-thumb {
        background: #B0A296;
        border-radius: 10px;
    }

    /* Individual Coffee Card */
    .coffee-card {
        flex: 0 0 240px;
        background-color: #3B2F2F;
        color: #FFFFFF;
        border-radius: 16px;
        padding: 40px 18px 18px 18px;
        position: relative;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    /* Overlapping Circular Badge */
    .coffee-circle-badge {
        position: absolute;
        top: -35px;
        left: 50%;
        transform: translateX(-50%);
        width: 70px;
        height: 70px;
        background-color: #4A3C3C;
        border: 4px solid #F5F0EB;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    }

    .card-title {
        color: #FFFFFF;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-top: 5px;
        margin-bottom: 6px;
        text-transform: uppercase;
        font-size: 1.05rem;
        line-height: 1.2;
    }

    .rating-badge {
        display: inline-block;
        background-color: #524343;
        color: #E2DBD3;
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 4px;
        margin-bottom: 8px;
        width: fit-content;
    }

    .card-desc {
        color: #C2B8B0;
        font-size: 0.82rem;
        margin-bottom: 12px;
        line-height: 1.3;
    }

    .price-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #2E2320;
        padding: 8px 12px;
        border-radius: 8px;
        border: 1px solid #4A3C3C;
        margin-top: auto;
    }

    .price-text {
        font-size: 1.15rem;
        font-weight: bold;
        color: #FFFFFF;
    }

    .add-btn {
        background-color: #E2DBD3;
        color: #231B18;
        width: 26px;
        height: 26px;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.1rem;
    }

    /* Chat bubble background & text color */
    .stChatMessage, 
    [data-testid="stChatMessageContent"], 
    .stChatMessage p, 
    .stChatMessage div, 
    .stChatMessage span, 
    .stChatMessage li, 
    .stChatMessage strong, 
    .stChatMessage em {
        color: #3B2F2F !important;
    }

    .stChatMessage {
        background-color: #ECE5DD !important;
        border-radius: 12px;
    }
</style>
"""


if hasattr(st, "html"):
    st.html(custom_css)
else:
    st.markdown(custom_css, unsafe_allow_html=True)

# Helper function to load menu data
def load_menu():
    try:
        with open("menu.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

menu_items = load_menu()

# ==========================================
# 1. TOP SECTION: OUR COFFEE MENU
# ==========================================
st.markdown("""
<div class="menu-header-container">
    <div class="menu-title">OUR COFFEE</div>
    <div class="menu-subtitle">There's always room for coffee, it's not just coffee, it's an experience.</div>
</div>
""", unsafe_allow_html=True)

if not menu_items:
    st.error("menu.json not found!")
else:
    cards_list = []
    for item in menu_items:
        card = f"""
        <div class="coffee-card">
            <div class="coffee-circle-badge">☕</div>
            <div>
                <div class="card-title">{item['name']}</div>
                <div class="rating-badge">★ 4.6</div>
                <div class="card-desc"><strong>Volume:</strong> 160 ml<br><i>{item['description']}</i></div>
            </div>
            <div class="price-row">
                <span class="price-text">${item['price']:.2f}</span>
                <div class="add-btn">+</div>
            </div>
        </div>
        """
        cards_list.append(card)

    slider_html = f'<div class="scroll-container">{"".join(cards_list)}</div>'
    
    if hasattr(st, "html"):
        st.html(slider_html)
    else:
        st.markdown(slider_html, unsafe_allow_html=True)

st.divider()

# ==========================================
# 2. BOTTOM SECTION: AI BARISTA CHATBOT
# ==========================================
st.subheader("☕ AI Barista Chatbot")
st.caption("Powered by Google ADK (Running Locally)")

# SESSION STATE INITIALIZATION
if "session_service" not in st.session_state:
    st.session_state.session_service = InMemorySessionService()

if not st.session_state.session_service.get_session_sync(
    app_name="agents",
    user_id="local_user",
    session_id="default_streamlit_session"
):
    st.session_state.session_service.create_session_sync(
        app_name="agents",
        user_id="local_user",
        session_id="default_streamlit_session"
    )

st.session_state.agent = get_barista_agent()
st.session_state.runner = Runner(
    app_name="agents",
    agent=st.session_state.agent,
    session_service=st.session_state.session_service
)



if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to our Coffee Shop! Browse our menu above and let me know if you have any questions!"}
    ]

# Display existing message history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User interaction input
if user_input := st.chat_input("Ask about our menu, recommendations, or allergens..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Barista is thinking..."):
            formatted_message = types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_input)]
            )
            
            output_text = ""
            try:
                events = st.session_state.runner.run(
                    user_id="local_user",
                    session_id="default_streamlit_session",
                    new_message=formatted_message
                )
                
                for event in events:
                    # 1. Check for standard content parts
                    if hasattr(event, "content") and event.content:
                        parts = getattr(event.content, "parts", [])
                        for part in parts:
                            text = getattr(part, "text", None)
                            if text:
                                output_text += text

                    # 2. Check for event.get_text() or direct text if parts yielded no text
                    if not output_text:
                        if hasattr(event, "get_text") and callable(event.get_text):
                            output_text += event.get_text() or ""
                        elif hasattr(event, "text") and event.text:
                            output_text += str(event.text)

                if not output_text:
                    output_text = "No text response produced by agent."

            except Exception as e:
                err_str = str(e)
                if "RESOURCE_EXHAUSTED" in err_str or "429" in err_str:
                    output_text = "⚠️ Rate limit reached (5 requests/min). Please wait a few seconds and try again."
                else:
                    output_text = f"⚠️ Error: {e}"

            st.write(output_text)



    st.session_state.messages.append({"role": "assistant", "content": output_text})