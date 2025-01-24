import os
import streamlit as st
from agents.director_agent import director

def delete_file(file_name, upload_dir="uploads"):
    file_path = os.path.join(upload_dir, file_name)
    try:
        os.remove(file_path)
        st.sidebar.success(f"File '{file_name}' deleted successfully!")
        director.knowledge.vector_db.delete_record_by_name(file_name.replace(".pdf", ""))
    except Exception as e:
        st.sidebar.error(f"Error deleting file '{file_name}': {e}")
    

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
        for file in files:
            col1, col2 = st.sidebar.columns([4, 1])
            col1.markdown(f"- {file}")
            if col2.button("🗑️", key=file):
                delete_file(file)
    else:
        st.sidebar.info("No files uploaded yet.")