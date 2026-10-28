from langchain_core.vectorstores import InMemoryVectorStore

from app.embeddings import get_embeddings
from app.ingest import load_pdf, split_docs

PDF_PATH = "data/docs/Simpo_Product_Knowledge_Reference.pdf"


def build_store():
    docs = load_pdf(PDF_PATH)
    chunks = split_docs(docs)
    store = InMemoryVectorStore(embedding=get_embeddings())
    store.add_documents(chunks)
    return store


if __name__ == "__main__":
    store = build_store()

    questions = [
        "prime minister of india",
        "Tell me about the app passbook?",
    ]

    for q in questions:
        print("\nQUESTION:", q)
        results = store.similarity_search_with_score(q, k=5)
        for doc, score in results:
            print(f"  score={score:.3f}  page={doc.metadata.get('page_label')}")
            print("  ", doc.page_content.replace("\n", " "))
