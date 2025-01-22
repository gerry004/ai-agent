from phi.knowledge.combined import CombinedKnowledgeBase
from phi.vectordb.pgvector import PgVector
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.knowledge.website import WebsiteKnowledgeBase

from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.vectordb.pgvector import PgVector

pdf_knowledge_base = PDFKnowledgeBase(
    path="uploads",
    # Table name: ai.pdf_documents
    vector_db=PgVector(
        table_name="pdf_documents",
        db_url="postgresql+psycopg2://ai:ai@localhost:5532/ai",
    ),
    reader=PDFReader(chunk=True),
)


website_knowledge_base = WebsiteKnowledgeBase(
    urls=["https://gerryyang.ie"],
    # Number of links to follow from the seed URLs
    max_links=10,
    # Table name: ai.website_documents
    vector_db=PgVector(
        table_name="website_documents",
        db_url="postgresql+psycopg2://ai:ai@localhost:5532/ai",
    ),
)

knowledge_base = CombinedKnowledgeBase(
    sources=[
        pdf_knowledge_base,
        website_knowledge_base,
    ],
    vector_db=PgVector(
        # Table name: ai.combined_documents
        table_name="combined_documents",
        db_url="postgresql+psycopg2://ai:ai@localhost:5532/ai",
    ),
)
