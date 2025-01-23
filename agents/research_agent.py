from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv

load_dotenv()

# duckduckgo: search the web for a given topic and return the url of results, maybe specifically blog posts
# parse_website: given the duckduckgo url, parse the content for the blog post and summarise it
# arxiv: search arxiv for maths, science, computer science, statistic related papers and return the pdf urls
# google_scholar: search google scholar and return related academic articles and pdf urls
# youtube: search youtube and return related video transcripts and urls

research_agent = Agent(
    name="Research Agent",
    role="Returns web results for a given topic.",
    tools=[DuckDuckGo()],
)
