import streamlit as st
import os
import fitz
from dotenv import load_dotenv
from google import genai
from google.genai import types
import time

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
st.title("Pragya AI")
user_input = st.chat_input("Your Message", accept_file = True, file_type = ["pdf"])

if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

if user_input:

    if user_input.files:
        uploaded_file = user_input.files[0]
        st.chat_message("user").write(f"Uploaded file 📄 {uploaded_file.name}")

        text = ""
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()

        response = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=[types.Content(role="user", parts=[types.Part(text=f"summarize the given text... {text}")])]
        )

        with st.chat_message("assistant"):
            placeholder=st.empty()
            result=""
            for chunk in response:
                if chunk.text:
                    result+=chunk.text
                    placeholder.markdown(result)
                    time.sleep(0.02)
            
    elif user_input.text:
        st.chat_message("user").write(user_input.text)
        user_msg = user_input.text
        st.session_state.chat_history.append(types.Content(role="user",parts=[types.Part(text=user_msg)]))
        context_window = st.session_state.chat_history[-10:]

        response = client.models.generate_content_stream(
        model = "gemini-2.5-flash",
        contents =context_window
    )
        
        with st.chat_message("assistant"):
            placeholder=st.empty()
            result=""
            for chunk in response:
                if chunk.text:
                    result+=chunk.text
                    placeholder.markdown(result)
                    time.sleep(0.02)

        st.session_state.chat_history.append(
            types.Content(role="model", parts=[types.Part(text=result)])
        )



st.sidebar.write("Chat History", st.session_state.chat_history)                
    
