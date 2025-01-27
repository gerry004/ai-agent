import os
import streamlit as st
from agents.director_agent import director


def delete_file(file_name, upload_dir="uploads"):
    file_path = os.path.join(upload_dir, file_name)
    try:
        os.remove(file_path)
        st.sidebar.success(f"File '{file_name}' deleted successfully!")
        director.knowledge.vector_db.delete_record_by_name(
            file_name.replace(".pdf", "")
        )
    except Exception as e:
        st.sidebar.error(f"Error deleting file '{file_name}': {e}")


def sidebar(options, upload_dir="uploads"):
    st.session_state.selected_bot = st.sidebar.selectbox("Choose a bot:", options)
    st.sidebar.title("Kowledge Bases")
    if st.session_state.selected_bot == "Content Generator":
        st.sidebar.write("Content Generator")
        st.sidebar.subheader("PDF Knowledge Base")
        uploaded_file = st.sidebar.file_uploader(
            "Drag and drop your file here", type="pdf"
        )
        if uploaded_file is not None:
            file_path = os.path.join(upload_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            st.sidebar.success(f"File '{uploaded_file.name}' saved!")
            # director.knowledge.load(recreate=False)
        st.sidebar.write("### Uploaded Files:")
        files = os.listdir(upload_dir)

        if files:
            for file in files:
                st.sidebar.write(f"- {file}")
        else:
            st.sidebar.write("No files uploaded yet.")

        st.sidebar.subheader("Website Knowledge Base")
        website_url = st.sidebar.text_input("Enter a website URL:")
        if website_url:
            st.sidebar.write(f"URL: {website_url}")
            # director.knowledge.load(recreate=False)
        
        # for website_url in website_urls:
        #     st.sidebar.write(f"- {website_url}")
      
    elif st.session_state.selected_bot == "Lead Gatherer":
        st.sidebar.write("Lead Gatherer")
    elif st.session_state.selected_bot == "Outreach Emailer":
        st.sidebar.write("Outreach Emailer")
