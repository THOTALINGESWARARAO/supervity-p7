import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


VECTORSTORE_DIR = Path("backend/vectorstore")

FAISS_INDEX_PATH = VECTORSTORE_DIR / "faiss.index"
METADATA_PATH = VECTORSTORE_DIR / "metadata.json"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def load_vectorstore():
    """Load the FAISS index and chunk metadata."""

    index = faiss.read_index(str(FAISS_INDEX_PATH))

    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    return index, metadata


def search(query: str, top_k: int = 3):
    """Search the vector store for the most relevant chunks."""

    model = SentenceTransformer(EMBEDDING_MODEL)

    index, metadata = load_vectorstore()

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    scores, indices = index.search(
        query_embedding.astype("float32"),
        top_k,
    )

    results = []

    for score, index_position in zip(scores[0], indices[0]):
        result = metadata[index_position].copy()
        result["score"] = float(score)

        results.append(result)

    return results


if __name__ == "__main__":
    query = "How many days do I have to enroll in health insurance?"

    results = search(query)

    print(f"\nQuery: {query}\n")

    for rank, result in enumerate(results, start=1):
        print(f"--- Result {rank} ---")
        print(f"Score: {result['score']:.4f}")
        print(f"Source: {result['source']}")
        print(f"Chunk: {result['chunk_index']}")
        print(f"Text: {result['text']}")
        print()