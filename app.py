import streamlit as st
from agents.director_agent import director
from dotenv import load_dotenv
load_dotenv()

# Streamlit app UI
st.title('Agent Yang')

# Initialize session state for conversation history if not already set
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display the conversation history
for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

# User input box
prompt = st.chat_input("Pass Your Prompt Here:")

if (prompt):
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    # Pass user input to the agent and get the response
    response = director.run(prompt, stream=False).content
    
    # Add the agent's response to the conversation history
    st.chat_message('assistant').markdown(response)
    st.session_state.messages.append({'role': 'assistant', 'content': response})
