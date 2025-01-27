import json
from typing import Optional, Iterator, Dict, List
from pydantic import BaseModel, Field
from phi.agent import Agent
from phi.workflow import Workflow, RunResponse, RunEvent
from phi.storage.workflow.sqlite import SqlWorkflowStorage
from phi.tools.googlesearch import GoogleSearch
from phi.tools.newspaper4k import Newspaper4k
from phi.utils.pprint import pprint_run_response
from phi.utils.log import logger
from dotenv import load_dotenv
import uuid
from phi.embedder.ollama import OllamaEmbedder
from phi.model.ollama import Ollama

load_dotenv()
import os

from phi.knowledge.website import WebsiteKnowledgeBase
from knowledge.pg_vector import PgVector

website_knowledge_base = WebsiteKnowledgeBase(
    urls=[],
    max_links=1,
    vector_db=PgVector(
        table_name="website_documents",
        db_url=os.getenv("DATABASE_URL"),
        embedder=OllamaEmbedder(model="nomic-embed-text"),
    ),
)

class Subheadings(BaseModel):
    subheadings: list[str] = Field(..., description="Subheadings for each section.")

class Article(BaseModel):
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="Link to the article.")

class SearchResults(BaseModel):
    articles: List[Article] = Field(..., description="List of articles found.")

class StringResponse(BaseModel):
    content: str = Field(..., description="Content generated.")

class ContentGenerator(Workflow):
    planner: Agent = Agent(
        model=Ollama(id="llama3.1"),
        instructions=[
            "Given a writing prompt, **think** and **plan** a structure for the content, return 5 subheadings.",
        ],
        response_model=Subheadings,
    )

    searcher: Agent = Agent(
        model=Ollama(id="llama3.1"),
        tools=[GoogleSearch()],
        show_tool_calls=True,
        instructions=[
            "You will be given a subheading for a piece of content.",
            "Use the google_search() tool to search for 3 articles related the subheading.",
            "Return the single most relevant article.",
        ],
        response_model=SearchResults,
    )
    
    writer: Agent = Agent(
        model=Ollama(id="llama3.1"),
        search_knowledge=True,
        knowledge_base=website_knowledge_base,
        instructions=[
            "You will be given a prompt and subbheadings, search in the knowledge base for articles related to the subheadings.",
            "Gather as much relevant information as possible.",
            "Only use information gathered from the knowledge base. Do not use other sources. Do not come up with your own sources.",
            "Write a piece of content for the prompt based on the information gathered. Make sure to include your sources.",
        ],
        response_model=StringResponse,
    )

    def plan_content(self, prompt: str) -> list[str]:
        logger.info("Planning the content...")
        try:
            planner_response: RunResponse = self.planner.run(prompt)
            if planner_response and isinstance(planner_response.content, Subheadings):
                logger.info("Subheadings generated")
                return planner_response.content
            logger.warning("Planner response invalid")
        except Exception as e:
            logger.error(f"Error in planner: {e}")
        return None
    
    def search_web_and_add_to_knowledge_base(self, subheadings: list[str]) -> bool:
        for subheading in subheadings:
            logger.info(f"Searching articles for {subheading}...")
            try:
              search_results: RunResponse = self.searcher.run(subheading)
              print(search_results)
              if search_results and isinstance(search_results, SearchResults):
                  logger.info(f"Searcher found {len(search_results.articles)} articles for {subheading}")
                  for article in search_results.articles:
                      website_knowledge_base.urls.append(article.url)
              else:
                  logger.warning("Searcher response invalid")
            except Exception as e:
                logger.error(f"Error in searcher: {e}")
                return False

        try:
            website_knowledge_base.load(recreate=True)
            logger.info("Articles added to knowledge base")
        except Exception as e:
            logger.error(f"Error loading articles to knowledge base: {e}")
            return False
        return True
    
    def write_content(self, prompt: str, subheadings: Subheadings) -> Optional[str]:
        logger.info("Writing content...")
        try:
            writer_response: RunResponse = self.writer.run(f"Prompt: {prompt} Subheadings: {subheadings}")
            if writer_response and isinstance(writer_response.content, str):
                logger.info("Content written")
                return writer_response.content
            logger.warning("Writer response invalid")
        except Exception as e:
            logger.error(f"Error in writer: {e}")
        return None

    def run(self, prompt: str) -> Iterator[RunResponse]:
        # if not prompt:
        #     logger.warning("No prompt provided")
        #     yield RunResponse(
        #         run_id=self.run_id,
        #         event=RunEvent.workflow_completed,
        #         content="No prompt provided. Workflow ended."
        #     )
        #     return

        # logger.info(f"Starting content generation for: {prompt}")

        # planner_result = self.plan_content(prompt)
        # if not planner_result:
        #     yield RunResponse(
        #         run_id=self.run_id,
        #         event=RunEvent.workflow_completed,
        #         content="Failed to plan content structure."
        #     )
        #     return

        # print(planner_result)

        searcher_result = self.search_web_and_add_to_knowledge_base(["korean culture"])
        print(searcher_result)

        # searcher_result = self.search_web_and_add_to_knowledge_base(planner_result)
        # if not searcher_result:
        #     yield RunResponse(
        #         run_id=self.run_id,
        #         event=RunEvent.workflow_completed,
        #         content="Failed to search articles."
        #     )
        #     return

        # print(searcher_result)
        # records = website_knowledge_base.vector_db.get_all_records()
        # print(records)
        # for record in records:
        #     print(record["id"], record["name"])

        # writer_result = self.write_content(prompt, planner_result)
        # if not writer_result:
        #     yield RunResponse(
        #         run_id=self.run_id,
        #         event=RunEvent.workflow_completed,
        #         content="Failed to write content."
        #     )
        #     return
        
        # # save writer result to a file in generated directory
        # with open(f"generated/{self.run_id}.txt", "w") as f:
        #     f.write(writer_result)

generate_content = ContentGenerator(
    session_id=f"generate-content-{uuid.uuid4()}",
    storage=SqlWorkflowStorage(
        table_name="generate_content_workflow",
        db_file="tmp/workflows.db",
    ),
)

# records = website_knowledge_base.vector_db.get_all_records()
# print(records)
# for record in records:
#     print(record["id"], record["name"])

prompt = "How to make a delicious pizza at home?"
blog_post = generate_content.run(prompt)
pprint_run_response(blog_post, markdown=True)


# embeddings = OllamaEmbedder(model="nomic-embed-text").get_embedding("The quick brown fox jumps over the lazy dog.")

# # Print the embeddings and their dimensions
# print(f"Embeddings: {embeddings[:5]}")
# print(f"Dimensions: {len(embeddings)}")
