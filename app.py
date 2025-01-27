from components.content import content
from components.sidebar import sidebar
import streamlit as st

BOTS = ["Content Generator", "Lead Gatherer", "Outreach Emailer"]

def app():
  if "selected_bot" not in st.session_state:
    st.session_state.selected_bot = "Content Generator"
  sidebar(options=BOTS)
  content()

app()


