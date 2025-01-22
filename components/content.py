import streamlit as st
from agents.director_agent import director
from dotenv import load_dotenv
load_dotenv()

def content():
  st.title('Agent Yang')

  if 'messages' not in st.session_state:
      st.session_state.messages = []

  for message in st.session_state.messages:
      st.chat_message(message['role']).markdown(message['content'])

  prompt = st.chat_input("Enter you message:")

  if (prompt):
      st.chat_message('user').markdown(prompt)
      st.session_state.messages.append({'role': 'user', 'content': prompt})

      response = director.run(prompt, stream=False).content
      
      st.chat_message('assistant').markdown(response)
      st.session_state.messages.append({'role': 'assistant', 'content': response})