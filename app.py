import streamlit as st
import os
import fitz
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEYS"))
model  = genai.GenerativeModel("gemini-1.5-flash-002")

st.title("Studify")
st.text("your study buddy here to help you... just upload your study material and lets conquer the exams!")
uploaded_file = st.file_uploader("Upload your PDF", type="PDF")

text = ""

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page in doc:
        out = page.get_text()
        text += out

prompt = f"""
think of yourself as a great explainer about the topic which the user will give... summarize the given text in a detailed manner
ask 5 follow up questions from the user about the topic of text he has uplaoded and the questions must be highly relevent, think of yourself as the teacher so that you undertand what topics are import for the exmas 
and explain the in the best way possible 
{text}
"""

response = model.generate_content(prompt)

st.write(response.text)