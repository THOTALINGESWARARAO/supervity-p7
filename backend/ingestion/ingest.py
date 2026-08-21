from pathlib import Path

from sentence_transformers import SentenceTransformer

import faiss
import numpy as np

VECTORSTORE_DIR = Path("backend/vectorstore")
FAISS_INDEX_PATH = VECTORSTORE_DIR / "faiss.index"
METADATA_PATH = VECTORSTORE_DIR / "metadata.json"

DOCUMENTS_DIR = Path("backend/data/hr_documents")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def extract_text_from_file(file_path: Path) -> str:
    """Read text from a document."""

    return file_path.read_text(encoding="utf-8")


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    """Split text into overlapping chunks without breaking words."""

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_words = []
    current_length = 0

    for paragraph in paragraphs:
        words = paragraph.split()

        for word in words:
            additional_length = len(word) + (
                1 if current_words else 0
            )

            if current_length + additional_length > chunk_size:
                if current_words:
                    chunks.append(" ".join(current_words))

                overlap_words = []
                overlap_length = 0

                for previous_word in reversed(current_words):
                    word_length = len(previous_word) + (
                        1 if overlap_words else 0
                    )

                    if overlap_length + word_length > chunk_overlap:
                        break

                    overlap_words.insert(0, previous_word)
                    overlap_length += word_length

                current_words = overlap_words + [word]
                current_length = len(" ".join(current_words))

            else:
                current_words.append(word)
                current_length += additional_length

    if current_words:
        chunks.append(" ".join(current_words))

    return chunks


def load_documents() -> list[dict]:
    """Load and chunk all HR documents."""

    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        text = extract_text_from_file(file_path)
        chunks = chunk_text(text)

        documents.append(
            {
                "source": file_path.name,
                "chunks": chunks,
            }
        )

    return documents


def generate_embeddings(documents: list[dict]):
    """Generate embeddings for every document chunk."""

    model = SentenceTransformer(EMBEDDING_MODEL)

    all_chunks = []
    metadata = []

    for document in documents:
        for chunk_index, chunk in enumerate(document["chunks"]):
            all_chunks.append(chunk)

            metadata.append(
                {
                    "source": document["source"],
                    "chunk_index": chunk_index,
                    "text": chunk,
                }
            )

    embeddings = model.encode(
        all_chunks,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    return embeddings, metadata


def build_faiss_index(embeddings: np.ndarray):
    """Build a FAISS index from normalized embeddings."""

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings.astype("float32"))

    return index


def save_vectorstore(index, metadata):
    """Save FAISS index and chunk metadata."""

    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(FAISS_INDEX_PATH))

    import json

    with open(METADATA_PATH, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    documents = load_documents()

    print(f"Found {len(documents)} documents.")

    embeddings, metadata = generate_embeddings(documents)

    print(f"Total chunks: {len(metadata)}")
    print(f"Embedding shape: {embeddings.shape}")
    print(f"Embedding dimension: {embeddings.shape[1]}")

    index = build_faiss_index(embeddings)

    print(f"FAISS index contains {index.ntotal} vectors.")

    save_vectorstore(index, metadata)

    print(f"\nFAISS index saved to: {FAISS_INDEX_PATH}")
    print(f"Metadata saved to: {METADATA_PATH}")