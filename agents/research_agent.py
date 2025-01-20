from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo

from dotenv import load_dotenv
load_dotenv()

research_agent = Agent(
    name="Research Agent",
    role="Returns web results for a given topic.",
    tools=[DuckDuckGo()],
)
