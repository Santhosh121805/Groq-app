import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# --- 1. Initial Setup ---
load_dotenv()  # Load .env file

# --- 2. Initialize Client ---
@st.cache_resource
def get_client():
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        st.error("API key not found. Please set OPENAI_API_KEY in .env or secrets")
        st.stop()
    return OpenAI(api_key=api_key)

client = get_client()

# --- 3. App Configuration ---
st.set_page_config(page_title="AI Swiss Army Knife", page_icon="🔮")
MODELS = {
    "GPT-3.5 Turbo": "gpt-3.5-turbo",
    "GPT-4": "gpt-4",
    "GPT-4 Turbo": "gpt-4-turbo-preview"
}

# --- 4. Sidebar Controls ---
with st.sidebar:
    st.title("⚙️ Settings")
    selected_model = st.selectbox("Model", list(MODELS.keys()), index=0)
    temperature = st.slider("Creativity", 0.0, 2.0, 0.7, help="Higher = more creative/random")
    max_tokens = st.slider("Max Tokens", 100, 2000, 500)
    
    st.divider()
    if st.button("🧹 Clear Chat"):
        st.session_state.clear()
        st.rerun()

# --- 5. Main App ---
st.title("🔮 AI Swiss Army Knife")
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📝 Summarize", "🎨 Generate Image", "📊 Analyze"])

# --- 6. Chat Tab ---
with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODELS[selected_model],
                    messages=st.session_state.messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                reply = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.chat_message("assistant").write(reply)
            except Exception as e:
                st.error(f"Error: {str(e)}")

# --- 7. Summarization Tab ---
with tab2:
    st.subheader("Text Summarization")
    text_to_summarize = st.text_area("Paste your text here:", height=200)
    
    if st.button("Summarize", key="summarize_btn"):
        if not text_to_summarize.strip():
            st.warning("Please enter some text")
        else:
            with st.spinner("Creating summary..."):
                try:
                    response = client.chat.completions.create(
                        model=MODELS[selected_model],
                        messages=[
                            {"role": "system", "content": "You are a helpful summarizer. Create a concise summary."},
                            {"role": "user", "content": f"Summarize this:\n\n{text_to_summarize}"}
                        ],
                        temperature=0.3,  # Lower temp for more factual summaries
                        max_tokens=max_tokens
                    )
                    st.subheader("Summary")
                    st.write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# --- 8. Image Generation Tab ---
with tab3:
    st.subheader("DALL·E Image Generation")
    image_prompt = st.text_input("Describe the image you want to create:")
    image_size = st.selectbox("Size", ["256x256", "512x512", "1024x1024"])
    
    if st.button("Generate Image", key="image_btn"):
        if not image_prompt.strip():
            st.warning("Please enter a prompt")
        else:
            with st.spinner("Generating image..."):
                try:
                    response = client.images.generate(
                        prompt=image_prompt,
                        n=1,
                        size=image_size
                    )
                    st.image(response.data[0].url, caption=image_prompt)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# --- 9. Analysis Tab ---
with tab4:
    st.subheader("Text Analysis")
    analysis_type = st.selectbox("Analysis Type", 
        ["Sentiment", "Key Points", "Translation", "Proofread"])
    text_to_analyze = st.text_area("Text to analyze:", height=200)
    
    if st.button("Analyze", key="analyze_btn"):
        if not text_to_analyze.strip():
            st.warning("Please enter some text")
        else:
            with st.spinner("Analyzing..."):
                try:
                    system_prompt = {
                        "Sentiment": "Analyze the sentiment of this text. Identify if it's positive, negative or neutral.",
                        "Key Points": "Extract the 3-5 most important points from this text.",
                        "Translation": "Translate this text to English while preserving the meaning.",
                        "Proofread": "Proofread this text and suggest improvements."
                    }[analysis_type]
                    
                    response = client.chat.completions.create(
                        model=MODELS[selected_model],
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": text_to_analyze}
                        ],
                        temperature=0.3
                    )
                    st.subheader("Results")
                    st.write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# --- 10. Footer ---
st.divider()
st.caption("Note: This app uses OpenAI's API. Your conversations may be used for quality improvement.")
