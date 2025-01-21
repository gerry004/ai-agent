from phi.agent import Agent
from knowledge_master import pdf_knowledge_base
from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    knowledge=pdf_knowledge_base,
    search_knowledge=True,
)

agent.knowledge.load(recreate=False)

agent.print_response("Give a summary of Gerry Yang's career")
