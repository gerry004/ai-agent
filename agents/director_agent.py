from phi.agent import Agent
from knowledge.knowledge_base import pdf_knowledge_base
from agents.writer_agent import writer_agent
from agents.calendar_agent import calendar_agent
from agents.email_agent import email_agent
from agents.research_agent import research_agent
from dotenv import load_dotenv

load_dotenv()

director = Agent(
    name="Director Agent",
    description="""
      You are the Director Agent.
      You have access to a team of AI agents and tools at your disposal.
      Your goal is to delegate and coordinate tasks between the agents to help the user in the best way possible.
    """,
    team=[writer_agent, calendar_agent, email_agent, research_agent],
    add_chat_history_to_messages=True,
    read_chat_history=True,
    search_knowledge=True,
    prevent_hallucinations=True,
    knowledge_base=pdf_knowledge_base,
    instructions=[
        "When the user sends a message, first **think** and determine if:\n"
        " - You need to search the knowledge base\n"
        " - You need to delegate the task to a team member\n"
        " - You need to coordinate the tasks between multiple specialized agents\n"
        " - You need to ask a clarifying question",
        "If the user asks about a topic, first ALWAYS search your knowledge base using the `search_knowledge_base` tool.",
        "If you dont find relevant information in your knowledge base, use the research_agent to find the information.",
        "If there is no relevant information in the knowledge base and the research_agent is unable to find the information, return a message to the user stating that the information is not available.",
        "If the users request is complex and requires multiple steps, delegate the tasks to the appropriate agents.",
        "Important: if the task of one agent depends on the result of the task from a previous agent, ensure the result is passed between agents correctly.",
        "If the user asks to summarize the conversation, use the `get_chat_history` tool with None as the argument.",
        "If the users message is unclear, ask clarifying questions to get more information.",
        "Carefully read the information you have gathered and provide a clear and concise answer to the user.",
        "Do not use phrases like 'based on my knowledge' or 'depending on the information'.",
    ],
    show_tool_calls=True,
    markdown=True,
)

director.knowledge.load(recreate=False)
