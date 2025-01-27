from phi.agent import Agent
from phi.model.openai import OpenAIChat
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
)

prompt = """
    Generate an essay plan for the topic 'The impact of social media on society'.
    Return the result as a list of subheadings, in the format:
    ["<subheading1>", "<subheading2>", "<subheading3>", "<subheading4>", "<subheading5>"]
"""

response = agent.run(prompt)
print(response.content)
