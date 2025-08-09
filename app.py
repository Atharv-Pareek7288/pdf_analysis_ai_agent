import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import fitz


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash-002")
response = model.generate_content("Explain why ai will take over humans in near future in one line.")
print (response.text)

st.title("PDF Analysing Agent")
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

text = ""

if uploaded_file is not None:
    with st.spinner("Reading your PDF..."):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()

        st.success("PDF loaded successfully!")
        st.write("Here's preview of the text: ")
        st.text(text[:1000])