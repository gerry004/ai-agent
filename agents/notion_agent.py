from phi.agent import Agent
from dotenv import load_dotenv

load_dotenv()

# list_items: list all items in a notion database
# create_item: create an item in a notion database
# update_item: update an item in a notion database
# delete_item: delete an item in a notion database

notion_agent = Agent(
    name="Notion Agent",
    role="A Notion assistant can list items in a database and create items in a database.",
    instructions=[
        """
        You are a Notion assistant. You can list items in a database and create items in a database.
        """
    ],
    tools=[],
    show_tool_calls=True,
)
