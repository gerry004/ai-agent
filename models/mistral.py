import time
from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.tools.googlesearch import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model=Ollama(id="mistral"),
    tools=[GoogleSearch()],
    show_tool_calls=True,
)

writer_prompt = """
    Generate an essay plan for the topic 'The impact of social media on society'.
    Return the result as a list of subheadings, in the format:
    ["<subheading1>", "<subheading2>", "<subheading3>", "<subheading4>", "<subheading5>"]
"""

searcher_prompt = """
    Search the web for 3 articles related to the title 'The impact of social media on society'.
    Return only the most relevant article, in the format:
    {
      title: "<title>",
      url: "<url>"
    }
    Do not return anything else.
"""

start_time = time.time()
response = agent.run(searcher_prompt)
end_time = time.time()

execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")
print(f"Response: {response.content}")
