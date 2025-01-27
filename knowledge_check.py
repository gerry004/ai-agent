from knowledge.pdf_knowledge_base import pdf_knowledge_base
from knowledge.website_knowledge_base import website_knowledge_base

knowledge_bases = {
    "pdf": pdf_knowledge_base,
    "website": website_knowledge_base,
}

def knowledge_check(knowledge_bases):
    for name, knowledge_base in knowledge_bases.items():
        print(f"Knowledge Base: {name}")
        records = knowledge_base.vector_db.get_all_records()
        unique_names = set([record["name"] for record in records])
        print(f"- Size: {len(records)} records")
        print(f"- Unique names:")
        for name in unique_names:
            print(f"   - {name}")
        print()

knowledge_check(knowledge_bases)