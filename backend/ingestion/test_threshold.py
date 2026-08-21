from retrieve import search


query = "How many days do I have to enroll in health insurance?"

results = search(
    query,
    top_k=5,
    score_threshold=0.30,
)

print(f"\nQuery: {query}\n")

if not results:
    print("No relevant results found.")
else:
    for rank, result in enumerate(results, start=1):
        print(
            f"{rank}. "
            f"{result['source']} | "
            f"chunk={result['chunk_index']} | "
            f"score={result['score']:.4f}"
        )