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
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

# User input box
user_input = st.text_input("Enter your command:")

if user_input:
    # Add the user input to the conversation history
    st.session_state['conversation_history'].append(f"User: {user_input}")

    # Pass user input to the agent and get the response
    response = agent.run(user_input, stream=False).content
    
    # Add the agent's response to the conversation history
    st.session_state['conversation_history'].append(f"Agent: {response}")

# Display the conversation history
for message in st.session_state['conversation_history']:
    st.write(message)
