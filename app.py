import streamlit as st
from phi.agent import Agent
from phi.tools.email import EmailTools
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the email tool
receiver_email = "gerry04y@gmail.com"
sender_email = "gerry04y@gmail.com"
sender_name = "Gerry Yang"
sender_passkey = "zqqdkqmcjpjqubif"

# Initialize the agent with email tools
agent = Agent(
    tools=[
        EmailTools(
            receiver_email=receiver_email,
            sender_email=sender_email,
            sender_name=sender_name,
            sender_passkey=sender_passkey,
        )
    ]
)

# Streamlit app UI
st.title('Chatbot: Email Assistant')

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
    response = agent.run(prompt, stream=False).content
    
    # Add the agent's response to the conversation history
    st.chat_message('assistant').markdown(response)
    st.session_state.messages.append({'role': 'assistant', 'content': response})
