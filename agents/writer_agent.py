from phi.agent import Agent
from dotenv import load_dotenv

load_dotenv()

# maybe a team, first ask the research_agent to find all the relevant articles, knowledge base pdfs, and blog posts, include sources
# then ask the writer_agent to write an article based on the provided sources
# harvard referencing style should be used

writer_agent = Agent(
    name="Writer Agent",
    role="Writes articles and blog posts based on provided details.",
    instructions=[
        """
        Include the topic, title, and body in the write_article tool.
        """
    ],
    tools=[],
)
