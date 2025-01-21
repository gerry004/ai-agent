from phi.agent import Agent
from tools.google_calendar import GoogleCalendarTools
import datetime
from tzlocal import get_localzone_name  # type: ignore

from dotenv import load_dotenv
load_dotenv()


calendar_agent = Agent(
    name="Calendar Agent",
    role="A Google Calendar assistant can list scheduled events and create events based on provided details.",
    instructions=[
        f"""
        You are scheduling assistant. Today is {datetime.datetime.now()} and the users timezone is {get_localzone_name()}.
        You should help users to perform these actions in their Google calendar:
            - get their scheduled events from a certain date and time, make sure date format is isoformat string
            - create events based on provided details
        """
    ],
    add_datetime_to_instructions=True,
    tools=[GoogleCalendarTools(token_path="../token.json")],
    show_tool_calls=True,
)
