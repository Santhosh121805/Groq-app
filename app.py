import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# --- 1. Initial Setup ---
load_dotenv()  # Load .env file

# --- 2. Enhanced Client Initialization ---
@st.cache_resource
def get_client():
    # Try all possible key sources in order of priority
    api_key = (
        st.secrets.get("openai", {}).get("api_key")  # Streamlit Cloud format
        or os.getenv("OPENAI_API_KEY")  # .env file
    )
    
    # Debug output (visible in terminal)
    print(f"Key loaded: {bool(api_key)}")
    
    if not api_key:
        st.error("""
        🔑 API key not found! Please:
        1. Add to .env: `OPENAI_API_KEY=sk-proj-...` (no quotes)
        2. Or set in Streamlit secrets (Settings → Secrets)
        """)
        st.stop()
        
    # Validate key format
    if not (api_key.startswith('sk-proj-') and len(api_key) in (51, 52, 53)):
        st.error("""
        🚨 Invalid API key format!
        • Should start with 'sk-proj-'
        • Should be 51-53 characters long
        • Get a new key: https://platform.openai.com/account/api-keys
        """)
        st.stop()
        
    return OpenAI(api_key=api_key.strip())

# --- 3. App Configuration ---
st.set_page_config(
    page_title="AI Swiss Army Knife",
    page_icon="🔮",
    layout="wide"
)

MODELS = {
    "GPT-3.5 Turbo": "gpt-3.5-turbo",
    "GPT-4": "gpt-4",
    "GPT-4 Turbo": "gpt-4-turbo-preview"
}

# --- 4. Sidebar with Key Verification ---
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Key status indicator
    try:
        client = get_client()
        client.models.list()  # Test connection
        st.success("✅ API Connected")
    except Exception as e:
        st.error(f"🔴 Connection Failed: {str(e)}")
        st.stop()
    
    selected_model = st.selectbox(
        "Model",
        list(MODELS.keys()),
        index=0
    )
    temperature = st.slider(
        "Creativity",
        0.0, 2.0, 0.7,
        help="Higher = more creative/random"
    )
    max_tokens = st.slider(
        "Max Tokens",
        100, 2000, 500,
        help="Maximum length of response"
    )
    
    if st.button("🧹 Clear Chat History"):
        st.session_state.clear()
        st.rerun()

# --- 5. Main App Tabs ---
st.title("🔮 AI Swiss Army Knife")
tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Chat", 
    "📝 Summarize", 
    "🎨 Generate Image", 
    "📊 Analyze"
])

# --- 6. Enhanced Chat Tab ---
with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        avatar = "🤖" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])
    
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt
        })
        
        with st.chat_message("user", avatar="👤"):
            st.write(prompt)
        
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODELS[selected_model],
                    messages=st.session_state.messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                reply = response.choices[0].message.content
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": reply
                })
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(reply)
            except Exception as e:
                st.error(f"🚨 Error: {str(e)}")
                st.info("Try clearing chat history or using a simpler prompt")

# [Rest of your tabs (Summarize, Generate Image, Analyze) remain the same...]

# --- 10. Deployment Instructions ---
with st.expander("🚀 Deployment Help"):
    st.markdown("""
    ### How to set up your API key:
    
    **For Local Development:**
    1. Create `.env` file in same folder as this script
    2. Add this line:
       ```bash
       OPENAI_API_KEY=sk-proj-your-key-here
       ```
    3. No quotes, no spaces!
    
    **For Streamlit Cloud:**
    1. Go to Settings → Secrets
    2. Add:
       ```toml
       [openai]
       api_key = "sk-proj-your-key-here"
       ```
    3. Redeploy your app
    """)

# Footer
st.divider()
st.caption("Note: API usage is logged by OpenAI for quality improvement")
