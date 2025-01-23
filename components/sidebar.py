import os
import streamlit as st
from agents.director_agent import director

def sidebar(upload_dir="uploads"):
    os.makedirs(upload_dir, exist_ok=True)

    st.sidebar.title("PDF Knowledge Base")
    uploaded_file = st.sidebar.file_uploader("Drag and drop your file here", type="pdf")

    if uploaded_file is not None:
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        st.sidebar.success(f"File '{uploaded_file.name}' saved!")
        director.knowledge.load(recreate=False)

    st.sidebar.write("### Uploaded Files:")
    files = os.listdir(upload_dir)

    if files:
        st.sidebar.markdown("\n".join(f"- {file}" for file in files))
    else:
        st.sidebar.info("No files uploaded yet.")
