import streamlit as st
import os
import fitz
from dotenv import load_dotenv
from google import genai
import time

load_dotenv()
api_key=os.getenv("GEMINI_API_KEYS")
client = genai.Client(api_key=api_key)
st.title("EchoLens")
user_input = st.chat_input("Your Message", accept_file = True, file_type = ["pdf"])

if user_input:

    if user_input.files:
        uploaded_file = user_input.files[0]
        st.chat_message("user").write(f"Uploaded file 📄 {uploaded_file.name}")

        text = ""
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            out = page.get_text()
            text += out

        response = client.models.generate_content_stream(
            model= "gemini-2.5-flash",
            contents = f"summarize the give text in such a way that it covers all the important topics ... {text}"

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

        response = client.models.generate_content_stream(
        model = "gemini-2.5-flash",
        contents =[user_input.text]
    )

        with st.chat_message("assistant"):
            placeholder=st.empty()
            result=""
            for chunk in response:
                if chunk.text:
                    result+=chunk.text
                    placeholder.markdown(result)
                    time.sleep(0.02)


