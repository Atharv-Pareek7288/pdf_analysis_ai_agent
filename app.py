import streamlit as st
import fitz

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