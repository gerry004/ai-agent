from knowledge.knowledge_base import pdf_knowledge_base

records = pdf_knowledge_base.vector_db.get_all_records()
for record in records:
    print(record["id"], record["name"])