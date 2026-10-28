from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.embeddings import get_embeddings

def load_pdf(path: str):
    loader = PyPDFLoader(path)
    return loader.load()


def split_docs(docs, chunk_size=800, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(docs)


if __name__ == "__main__":
    docs = load_pdf("data/docs/Simpo_Product_Knowledge_Reference.pdf")
    chunks = split_docs(docs)

    lengths = [len(c.page_content) for c in chunks]

    emb = get_embeddings()

    # 1. embed one chunk
    vec = emb.embed_query(chunks[0].page_content)
    print("dimension:", len(vec))
    print("first 5 numbers:", vec[:5])

    # 2. embed all chunks at once
    texts = [c.page_content for c in chunks]
    vectors = emb.embed_documents(texts)
    print("chunks:", len(texts), "vectors:", len(vectors))

