from phi.agent import Agent
from tools.send_email import send_email

from dotenv import load_dotenv
load_dotenv()

email_agent = Agent(
    name="Email Agent",
    role="Sends email to users via send_email tool.",
    instructions=[
        """
        Include receiver email, subject, and body in send_email tool.
        """
    ],
    tools=[send_email],
)
