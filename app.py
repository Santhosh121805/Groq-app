import streamlit as st
st.write("🔄 Debug: App started successfully")  # Should appear immediately
import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Debug: Uncomment to verify (check terminal)
# print("Current directory:", os.getcwd())
# print("Files present:", os.listdir())
# print("Key exists:", "OPENAI_API_KEY" in os.environ)

# --- 2. Key Validation ---
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("""
    ❌ Key missing! Verify:
    1. .env exists in same folder as this script
    2. Contains: OPENAI_API_KEY=sk-...
    3. No typos or spaces
    """)
    st.stop()

# --- 3. Initialize OpenAI ---
try:
    client = OpenAI(api_key=api_key)
    # Quick connection test
    client.models.list()
    st.success("✅ OpenAI Connected!")
except Exception as e:
    st.error(f"""
    🔌 Connection failed: {str(e)}
    
    Fixes:
    1. Check key at platform.openai.com/account/api-keys
    2. Restart this app
    3. Check https://status.openai.com for outages
    """)
    st.stop()

# --- 4. Your App ---
st.title("🌐 AI Assistant Ready!")
st.write("API key loaded successfully")

# Add your features here
if st.button("Test Connection"):
    models = client.models.list()
    st.write(f"Available models: {len(models.data)}")
