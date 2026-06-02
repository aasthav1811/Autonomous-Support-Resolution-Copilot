import os
import glob
import chromadb
from chromadb.utils import embedding_functions
from src.config import CHROMA_PERSIST_DIR, COLLECTION_NAME, EMBEDDING_MODEL


def chunk_markdown(text: str) -> list:
    """Split by ## headers for semantic chunks."""
    chunks = []
    sections = text.split("## ")
    for section in sections:
        section = section.strip()
        if section and len(section) > 30:  # skip tiny fragments
            chunks.append(section)
    return chunks


def ingest_knowledge_base(kb_dir: str = "data/knowledge_base"):
    print(f"Loading embedding model: {EMBEDDING_MODEL} (downloading once if not cached)...")
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )

    # Reset collection fresh each ingest
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn,
    )

    docs, ids, metas = [], [], []
    md_files = glob.glob(os.path.join(kb_dir, "*.md"))

    if not md_files:
        print(f"⚠️  No .md files found in {kb_dir}. Create them first!")
        return collection

    for filepath in md_files:
        category = os.path.basename(filepath).replace("_faq.md", "")
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = chunk_markdown(text)
        for i, chunk in enumerate(chunks):
            docs.append(chunk)
            ids.append(f"{category}_{i}")
            metas.append({"category": category, "source": os.path.basename(filepath)})

    collection.add(documents=docs, ids=ids, metadatas=metas)
    print(f"✅ Ingested {len(docs)} chunks from {len(md_files)} files into ChromaDB.")
    return collection


if __name__ == "__main__":
    ingest_knowledge_base()
