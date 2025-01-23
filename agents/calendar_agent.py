from phi.agent import Agent
from tools.google_calendar_tools import GoogleCalendarTools
import datetime
from tzlocal import get_localzone_name  # type: ignore
from dotenv import load_dotenv

load_dotenv()

# list_events_from: from a certain date and time
# list_events_between: between two dates and times
# categorise_events_color: categorise events based on their color
# categorise_events_ai: categorise events based on their title
# find_available_time_slot: find available time slots between two dates and times
# find_all_gap_times: find gaps for a certain timeframe calculated between the start of the first event of that timeframe and the end of the last event of that timeframe
# create_event: create an event based on provided details
# update_event: update an event based on provided details
# delete_event: delete an event based on provided details


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
