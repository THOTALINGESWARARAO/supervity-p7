import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


VECTORSTORE_DIR = Path("backend/vectorstore")

FAISS_INDEX_PATH = VECTORSTORE_DIR / "faiss.index"
METADATA_PATH = VECTORSTORE_DIR / "metadata.json"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class RAGRetriever:
    """Semantic retriever backed by a FAISS vector store."""

    def __init__(
        self,
        index_path: Path = FAISS_INDEX_PATH,
        metadata_path: Path = METADATA_PATH,
        embedding_model: str = EMBEDDING_MODEL,
    ):
        self.index_path = index_path
        self.metadata_path = metadata_path

        # Load expensive resources once.
        self.model = SentenceTransformer(embedding_model)
        self.index = faiss.read_index(str(index_path))

        with open(metadata_path, "r", encoding="utf-8") as file:
            self.metadata = json.load(file)

    def search(
        self,
        query: str,
        top_k: int = 3,
        score_threshold: float | None = None,
    ) -> list[dict]:
        """Return the most relevant chunks for a query."""

        if not query.strip():
            raise ValueError("Query must not be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0.")

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        scores, indices = self.index.search(
            query_embedding.astype("float32"),
            top_k,
        )

        results = []

        for score, index_position in zip(scores[0], indices[0]):
            # FAISS can return -1 when no valid result exists.
            if index_position < 0:
                continue

            # Protect against invalid metadata references.
            if index_position >= len(self.metadata):
                continue

            score = float(score)

            if (
                score_threshold is not None
                and score < score_threshold
            ):
                continue

            result = self.metadata[index_position].copy()
            result["score"] = score

            results.append(result)

        return results


# Load the retriever once when this module is imported.
retriever = RAGRetriever()


def search(
    query: str,
    top_k: int = 3,
    score_threshold: float | None = None,
) -> list[dict]:
    """Convenience function for semantic search."""

    return retriever.search(
        query=query,
        top_k=top_k,
        score_threshold=score_threshold,
    )


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