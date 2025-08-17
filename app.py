import streamlit as st
import os
import fitz
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key=os.getenv("GEMINI_API_KEYS")
client = genai.Client(api_key=api_key)

user_input = st.chat_input("Your Message", accept_file = True, file_type = ["pdf"])

if user_input:
    st.chat_message("user").write(user_input.text)

    response = client.models.generate_content_stream(
    model = "gemini-2.5-flash",
    contents =user_input.text
)

    with st.chat_message("assistant"):
        result=""
        for chunk in response:
            if chunk.text:
                result+=chunk.text
        st.write(result)
text = ""
#added the pdf uploading system inside the chatbox... just like the chatgpt 
if user_input and user_input.files:
    uploaded_file = user_input.files[0]
    dov = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page in dov:
        out = page.get_text()
        text += out
st.chat_message("assistant").write(text)
