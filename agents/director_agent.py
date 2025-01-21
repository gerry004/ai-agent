from phi.agent import Agent
from phi.knowledge import AgentKnowledge
from phi.tools.duckduckgo import DuckDuckGo
from agents.calendar_agent import calendar_agent
from agents.email_agent import email_agent
from agents.research_agent import research_agent

from dotenv import load_dotenv
load_dotenv()

director = Agent(
    name="Director Agent",
    description="""
      You are the Director Agent.
      You have access to a set of tools and a team of AI agents at your disposal.
      Your goal is to assist the user in the best way possible.
    """,
    team=[calendar_agent, email_agent, research_agent],
    tools=[DuckDuckGo()],
    read_chat_history=True,
    search_knowledge=True,
    prevent_hallucinations=True,
    knowledge_base=AgentKnowledge(),
    instructions=[
        "When the user sends a message, first **think** and determine if:\n"
        " - You can answer by using a tool available to you\n"
        " - You need to search the knowledge base\n"
        " - You need to search the internet\n"
        " - You need to delegate the task to a team member\n"
        " - You need to coordinate the tasks between multiple specialized agents\n"
        " - You need to ask a clarifying question",
        "If the user asks about a topic, first ALWAYS search your knowledge base using the `search_knowledge_base` tool.",
        "If you dont find relevant information in your knowledge base, use the `duckduckgo_search` tool to search the internet.",
        "If the user asks to summarize the conversation, use the `get_chat_history` tool with None as the argument.",
        "If the users message is unclear, ask clarifying questions to get more information.",
        "Carefully read the information you have gathered and provide a clear and concise answer to the user.",
        "Do not use phrases like 'based on my knowledge' or 'depending on the information'.",
        "Important: if the task of one agent depends on the result of the task from a previous agent, make sure the result is passed on accordingly, if needed.",
    ],
    show_tool_calls=True,
    markdown=True,
)
