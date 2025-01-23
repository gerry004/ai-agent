from phi.tools import Toolkit
from phi.utils.log import logger
import datetime
import os.path
import json
from functools import wraps

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
    from googleapiclient.discovery import build  # type: ignore
    from googleapiclient.errors import HttpError  # type: ignore
except ImportError:
    raise ImportError(
        "Google client library for Python not found , install it using `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`"
    )
from typing import List, Optional
import os

SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Hardcoded credentials (replace with your actual credentials)
CREDENTIALS = {
    "installed": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "project_id": "phidata-448319",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uris": ["http://localhost"],
    }
}


def authenticated(func):
    """Decorator to ensure authentication before executing the method."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Ensure credentials are valid
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(CREDENTIALS, SCOPES)
                self.creds = flow.run_local_server(port=0)
                # Save the credentials for future use
            with open(self.token_path, "w") as token:
                token.write(self.creds.to_json())

            # Initialize the Google Calendar service
        try:
            self.service = build("calendar", "v3", credentials=self.creds)
        except HttpError as error:
            logger.error(f"An error occurred while creating the service: {error}")
            raise

        # Ensure the service is available
        if not self.service:
            raise ValueError("Google Calendar service could not be initialized.")

        return func(self, *args, **kwargs)

    return wrapper


class GoogleCalendarTools(Toolkit):
    def __init__(self, token_path: Optional[str] = None):
        """
        Google Calendar Tool.

        :param token_path: Path of the file token.json which stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.

        """
        super().__init__(name="google_calendar_tools")

        if not token_path:
            logger.warning(
                f"Google Calendar Tool : Token path is not provided, using {os.getcwd()}/token.json as default path"
            )
            token_path = "token.json"

        self.creds = None
        self.service = None
        self.token_path = token_path
        self.register(self.list_events)
        self.register(self.create_event)

    @authenticated
    def list_events(
        self, limit: int = 10, date_from: str = datetime.date.today().isoformat()
    ) -> str:
        """
        List events from the user's primary calendar.

        Args:
            limit (Optional[int]): Number of events to return , default value is 10
            date_from (str) : the start date to return events from in date isoformat. Defaults to current datetime.

        """
        if date_from is None:
            date_from = datetime.datetime.now(datetime.timezone.utc).isoformat()
        elif isinstance(date_from, str):
            date_from = datetime.datetime.fromisoformat(date_from).strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )

        try:
            if self.service:
                events_result = (
                    self.service.events()
                    .list(
                        calendarId="primary",
                        timeMin=date_from,
                        maxResults=limit,
                        singleEvents=True,
                        orderBy="startTime",
                    )
                    .execute()
                )
                events = events_result.get("items", [])
                if not events:
                    return json.dumps({"error": "No upcoming events found."})
                return json.dumps(events)
            else:
                return json.dumps({"error": "authentication issue"})
        except HttpError as error:
            return json.dumps({"error": f"An error occurred: {error}"})

    @authenticated
    def list_events_between(self, date_from: str, date_to: str, limit: int = 10) -> str:
        """
        List events between two dates from the user's primary calendar.

        Args:
            date_from (str) : the start date to return events from in date isoformat
            date_to (str) : the end date to return events from in date isoformat
            limit (Optional[int]): Number of events to return , default value is 10
        """
        pass

    @authenticated
    def create_event(
        self,
        start_datetime: str,
        end_datetime: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        timezone: Optional[str] = None,
        attendees: List[str] = [],
    ) -> str:
        """
        Create a new event in the user's primary calendar.

        Args:
            title (Optional[str]): Title of the Event
            description (Optional[str]) : Detailed description of the event
            location (Optional[str]) : Location of the event
            start_datetime (Optional[str]) : start date and time of the event
            end_datetime (Optional[str]) : end date and time of the event
            attendees (Optional[List[str]]) : List of emails of the attendees
        """

        attendees_list = (
            [{"email": attendee} for attendee in attendees] if attendees else []
        )

        start_time = datetime.datetime.fromisoformat(start_datetime).strftime(
            "%Y-%m-%dT%H:%M:%S"
        )

        end_time = datetime.datetime.fromisoformat(end_datetime).strftime(
            "%Y-%m-%dT%H:%M:%S"
        )
        try:
            event = {
                "summary": title,
                "location": location,
                "description": description,
                "start": {"dateTime": start_time, "timeZone": timezone},
                "end": {"dateTime": end_time, "timeZone": timezone},
                "attendees": attendees_list,
            }
            if self.service:
                event_result = (
                    self.service.events()
                    .insert(calendarId="primary", body=event)
                    .execute()
                )
                return json.dumps(event_result)
            else:
                return json.dumps({"error": "authentication issue"})
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            return json.dumps({"error": f"An error occurred: {error}"})

    # update_event: update an event based on provided details
    # delete_event: delete an event based on provided details


    # categorise_events_color: categorise events based on their color
    # categorise_events_ai: categorise events based on their title
    # find_available_time_slot: find available time slots between two dates and times
    # find_all_gap_times: find gaps for a certain timeframe calculated between the start of the first event of that timeframe and the end of the last event of that timeframe


# gcal = GoogleCalendarTools(token_path="token.json")
# events = gcal.list_events()
# for event in json.loads(events):
#     print(event["summary"])
