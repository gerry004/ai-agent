from phi.vectordb.pgvector import PgVector
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from knowledge.pg_vector import PgVector
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

pdf_knowledge_base = PDFKnowledgeBase(
    path="uploads",
    vector_db=PgVector(
        table_name="pdf_documents",
        db_url=DATABASE_URL,
    ),
    reader=PDFReader(chunk=True),
)


records = pdf_knowledge_base.vector_db.get_all_records()
for record in records:
    print(record["name"])