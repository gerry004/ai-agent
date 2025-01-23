from phi.knowledge.combined import CombinedKnowledgeBase
from phi.vectordb.pgvector import PgVector
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.knowledge.website import WebsiteKnowledgeBase
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.vectordb.pgvector import PgVector
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")

pdf_knowledge_base = PDFKnowledgeBase(
    path="uploads",
    vector_db=PgVector(
        table_name="pdf_documents",
        db_url=DATABASE_URL,
    ),
    reader=PDFReader(chunk=True),
)


website_knowledge_base = WebsiteKnowledgeBase(
    urls=["https://gerryyang.ie"],
    max_links=10,
    vector_db=PgVector(
        table_name="website_documents",
        db_url=DATABASE_URL,
    ),
)

knowledge_base = CombinedKnowledgeBase(
    sources=[
        pdf_knowledge_base,
        website_knowledge_base,
    ],
    vector_db=PgVector(
        table_name="combined_documents",
        db_url=DATABASE_URL,
    ),
)
