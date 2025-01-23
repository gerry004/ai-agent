import httpx
from phi.tools import Toolkit
import os

from dotenv import load_dotenv
load_dotenv()


class EmailTools(Toolkit):
    def __init__(
        self,
        database_id: str = "184bed9901cd80acb77df4fdeb9182ce",
    ):
        """
        Email Tool.

        :param database_id (str): ID of the database, default id exists
        """
        super().__init__(name="email_tools")

        if not database_id:
            return "error: No database id provided"

        self.database_id = database_id
        self.database_url = f"https://api.notion.com/v1/databases/{database_id}/query"
        self.register(self.get_items)

    def get_items(self) -> str:
        """
        List all items in the notion database.

        """
        results = httpx.post(
            self.database_url,
            headers={"Authorization": f"Bearer {os.getenv("NOTION_API_KEY")}", "Notion-Version": "2022-06-28"},
        )

        result_dict = results.json()
        return result_dict["results"]

    def create_item():
        pass

    def update_item():
        pass

    def delete_item():
        pass


# list_items: list all items in a notion database
# create_item: create an item in a notion database
# update_item: update an item in a notion database
# delete_item: delete an item in a notion database
