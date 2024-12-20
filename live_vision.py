import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64

def get_api_key():
    # Encoded API key (encode your key first using base64)
    encoded_key = "your api key"  # This is just an example
    # Decode the key when needed
    return base64.b64decode(encoded_key).decode('utf-8')

def initialize_gemini():
    api_key = get_api_key()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

# Set up the Streamlit App
st.set_page_config(
    page_title="Multimodal Chatbot with Gemini Flash",
    layout="wide"
)
st.title("Multimodal Chatbot with Google gemini-2.0-flash-exp  ⚡️")
st.caption("Chat with Google's Gemini Flash model using image and text input to by Martin Khristi. 🌟")

# Initialize model
model = initialize_gemini()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for image upload
with st.sidebar:
    st.title("Chat with Images")
    uploaded_file = st.file_uploader(
        "Upload an image...",
        type=["jpg", "jpeg", "png"]
    )
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

# Main chat interface
chat_placeholder = st.container()

with chat_placeholder:
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input handling
prompt = st.chat_input("What do you want to know?")

if prompt:
    inputs = [prompt]
    
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    # Display user message
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(prompt)
    
    if uploaded_file:
        inputs.append(image)
    
    # Generate and display response
    with st.spinner('Generating response...'):
        try:
            response = model.generate_content(inputs)
            with chat_placeholder:
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                    
            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.text
            })
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

elif uploaded_file:
    st.warning("Please enter a text query to accompany the image.")