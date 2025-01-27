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

load_dotenv()

class Section(BaseModel):
    subheading: str = Field(..., description="Subheading for the section.")
    keywords: List[str] = Field(
        ..., description="Keywords as a search query for articles related to the section."
    )

class ContentStructure(BaseModel):
    sections: List[Section] = Field(..., description="Sections with subheadings and keywords.")

class Article(BaseModel):
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="Link to the article.")

class SearchResults(BaseModel):
    articles: List[Article] = Field(..., description="List of articles found.")

class ArticleWithSummary(Article):
    summary: str = Field(..., description="Summary of the article.")

class SearchResultsWithSummary(SearchResults):
    articles: List[ArticleWithSummary] = Field(..., description="List of articles with summaries.")

class ContentGenerator(Workflow):
    planner: Agent = Agent(
        instructions=[
            "Given a writing prompt, **think** and **plan** a structure for the content.",
            "Include subheadings for each section and 3 of the most relevant keywords for each subheading.",
            "Make each keyword a search query to find articles for that subheading section.",
        ],
        response_model=ContentStructure,
    )

    searcher: Agent = Agent(
        tools=[GoogleSearch()],
        instructions=[
            "Given a keyword, search for 10 articles and return the 3 most relevant articles."
        ],
        response_model=SearchResults,
    )

    reader: Agent = Agent(
        tools=[Newspaper4k()],
        instructions=[
            "Given the title and URL of the article, read the content of the article and explain the key points clearly.",
        ],
        response_model=ArticleWithSummary,
    )

    writer: Agent = Agent(
        instructions=[
            "You will be provided with a list of subheadings and articles with summaries for that subheading.",
            "Carefully read the information you have been given and write a compelling, clear, concise piece of content.",
            "Always provide sources, do not make up information or sources.",
        ],
    )

    def plan_content_structure(self, prompt: str) -> Optional[ContentStructure]:
        logger.info("Planning the content structure")
        try:
            planner_response: RunResponse = self.planner.run(prompt)
            if planner_response and isinstance(planner_response.content, ContentStructure):
                logger.info("Planner response valid")
                return planner_response.content
            logger.warning("Planner response invalid")
        except Exception as e:
            logger.error(f"Error in planner: {e}")
        return None

    def search_articles(self, keyword: str) -> Optional[SearchResults]:
        logger.info(f"Searching articles for: {keyword}")
        try:
            searcher_response: RunResponse = self.searcher.run(keyword)
            if searcher_response and isinstance(searcher_response.content, SearchResults):
                logger.info(f"Searcher found articles for: {keyword}")
                return searcher_response.content
            logger.warning("Searcher response invalid")
        except Exception as e:
            logger.error(f"Error in searcher: {e}")
        return None

    def read_article(self, article: Article) -> Optional[ArticleWithSummary]:
        logger.info(f"Reading article: {article.title}")
        try:
            reader_response: RunResponse = self.reader.run(article.url)
            if reader_response and isinstance(reader_response.content, ArticleWithSummary):
                summary = reader_response.content
                summary.title = article.title
                summary.url = article.url
                return summary
            logger.warning("Reader response invalid")
        except Exception as e:
            logger.error(f"Error in reader: {e}")
        return None

    def write_content(self, subheading_articles_dict: Dict[str, List[ArticleWithSummary]]) -> Optional[str]:
        logger.info("Writing the content")
        try:
            writer_response: RunResponse = self.writer.run(subheading_articles_dict)
            if writer_response and writer_response.content:
                logger.info("Content written successfully")
                return writer_response.content
            logger.warning("Writer response invalid")
        except Exception as e:
            logger.error(f"Error in writer: {e}")
        return None

    def run(self, prompt: str) -> Iterator[RunResponse]:
        if not prompt:
            logger.warning("No prompt provided")
            yield RunResponse(
                run_id=self.run_id,
                event=RunEvent.workflow_completed,
                content="No prompt provided. Workflow ended."
            )
            return

        logger.info(f"Starting content generation for: {prompt}")

        planner_result = self.plan_content_structure(prompt)
        if not planner_result:
            yield RunResponse(
                run_id=self.run_id,
                event=RunEvent.workflow_completed,
                content="Failed to plan content structure."
            )
            return

        subheading_articles_dict: Dict[str, List[ArticleWithSummary]] = {}

        for section in planner_result.sections:
            subheading = section.subheading
            subheading_articles_dict[subheading] = []
            for keyword in section.keywords:
                search_results = self.search_articles(keyword)
                if search_results:
                    for article in search_results.articles:
                        summary = self.read_article(article)
                        if summary:
                            subheading_articles_dict[subheading].append(summary)

        content = self.write_content(subheading_articles_dict)
        if content:
            yield RunResponse(
                run_id=self.run_id,
                event=RunEvent.workflow_completed,
                content=content,
            )
        else:
            yield RunResponse(
                run_id=self.run_id,
                event=RunEvent.workflow_completed,
                content="Failed to generate content."
            )

# Create and run the workflow
topic = "Korean language and culture"
generate_blog_post = ContentGenerator(
    session_id=f"generate-blog-post-on-{topic}",
    storage=SqlWorkflowStorage(
        table_name="generate_blog_post_workflows",
        db_file="tmp/workflows.db",
    ),
)

blog_post = generate_blog_post.run(prompt=topic)
pprint_run_response(blog_post, markdown=True)
