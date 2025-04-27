import streamlit as st
import os
from dotenv import load_dotenv
import openai

# --- 1. Environment Setup ---
load_dotenv()  # Load .env file

# --- 2. Key Validation ---
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("""
    ❌ Key missing! Verify:
    1. .env exists in the same folder as this script
    2. Contains: OPENAI_API_KEY=sk-...
    3. No typos or spaces
    """)
    st.stop()

# --- 3. Initialize OpenAI ---
try:
    openai.api_key = api_key
    models = openai.Model.list()  # Test connection by listing models
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

# --- 5. Text Generation ---
st.header("Text Generation")
user_input = st.text_area("Enter a prompt for text generation:", "Once upon a time...")
if st.button("Generate Text"):
    with st.spinner('Generating text...'):
        try:
            response = openai.Completion.create(
                model="text-davinci-003",  # You can change to another model
                prompt=user_input,
                max_tokens=100
            )
            st.write("Generated Text:")
            st.write(response.choices[0].text.strip())
        except Exception as e:
            st.error(f"Error generating text: {str(e)}")

# --- 6. Text Summarization ---
st.header("Text Summarization")
long_text = st.text_area("Enter text to summarize:")
if st.button("Summarize"):
    with st.spinner('Summarizing text...'):
        try:
            response = openai.Completion.create(
                model="text-davinci-003",  # Use a model suitable for summarization
                prompt=f"Summarize this text: {long_text}",
                max_tokens=150
            )
            st.write("Summary:")
            st.write(response.choices[0].text.strip())
        except Exception as e:
            st.error(f"Error summarizing text: {str(e)}")

# --- 7. Sentiment Analysis ---
st.header("Sentiment Analysis")
sentiment_input = st.text_area("Enter text for sentiment analysis:")
if st.button("Analyze Sentiment"):
    with st.spinner('Analyzing sentiment...'):
        try:
            response = openai.Completion.create(
                model="text-davinci-003",  # Use any model suitable for sentiment analysis
                prompt=f"Analyze the sentiment of the following text: {sentiment_input}",
                max_tokens=60
            )
            st.write("Sentiment Analysis Result:")
            st.write(response.choices[0].text.strip())
        except Exception as e:
            st.error(f"Error analyzing sentiment: {str(e)}")

# --- 8. Image Generation (Optional, using DALL·E or similar models) ---
st.header("Image Generation (Optional)")
image_prompt = st.text_area("Enter a prompt to generate an image:")
if st.button("Generate Image"):
    with st.spinner('Generating image...'):
        try:
            response = openai.Image.create(
                prompt=image_prompt,
                n=1,
                size="256x256"  # Choose the size of the generated image
            )
            st.image(response['data'][0]['url'], caption="Generated Image")
        except Exception as e:
            st.error(f"Error generating image: {str(e)}")

# --- 9. Question Answering ---
st.header("Question Answering")
question_input = st.text_area("Ask a question:")
if st.button("Get Answer"):
    with st.spinner('Fetching answer...'):
        try:
            response = openai.Completion.create(
                model="text-davinci-003",  # You can change to any Q&A model
                prompt=f"Answer the following question: {question_input}",
                max_tokens=100
            )
            st.write("Answer:")
            st.write(response.choices[0].text.strip())
        except Exception as e:
            st.error(f"Error answering question: {str(e)}")
