import os
from phi.knowledge.website import WebsiteKnowledgeBase
from knowledge.pg_vector import PgVector
from phi.embedder.ollama import OllamaEmbedder
from dotenv import load_dotenv

load_dotenv()

website_knowledge_base = WebsiteKnowledgeBase(
    urls=[],
    max_links=1,
    vector_db=PgVector(
        table_name="website_documents",
        db_url=os.getenv("DATABASE_URL"),
        embedder=OllamaEmbedder(model="nomic-embed-text"),
    ),
)