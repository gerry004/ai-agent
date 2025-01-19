from phi.agent import Agent
from phi.tools.email import EmailTools

from dotenv import load_dotenv
load_dotenv()

receiver_email = "gerry04y@gmail.com"
sender_email = "gerry04y@gmail.com"
sender_name = "Gerry Yang"
sender_passkey = "zqqdkqmcjpjqubif"

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
agent.print_response("Send an email to gerry04y@gmail.com with the subject 'Hello' and the message 'Hello, Gerry!'", stream=True)
