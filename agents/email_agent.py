from phi.agent import Agent
from tools.email_tools import EmailTools
from dotenv import load_dotenv

load_dotenv()

# send_email: send an email to a recipient with subject and body
# schedule_send_email: schedule an email to be sent at a specific time
# check_email: check email inbox for new messages related to certain keywords
# archive_email: archive emails in inbox

email_agent = Agent(
    name="Email Agent",
    role="Sends email to users via send_email tool.",
    instructions=[
        """
        Include receiver email, subject, and body in send_email tool.
        """
    ],
    tools=[
        EmailTools(
            sender_email="gerry04y@gmail.com",
            sender_name="Gerry Yang",
            sender_passkey="zqqdkqmcjpjqubif",
        )
    ],
)
