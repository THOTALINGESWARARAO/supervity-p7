from ingestion.retrieve import search


queries = [
    "How many days do I have to enroll in health insurance?",
    "What benefits are available to employees?",
    "What should I do if I receive a suspicious email?",
    "How do I set up my company laptop?",
    "What are the rules for employee passwords?",
]


for query in queries:
    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    results = search(query, top_k=3)

    for rank, result in enumerate(results, start=1):
        print(
            f"\n{rank}. "
            f"{result['source']} | "
            f"chunk={result['chunk_index']} | "
            f"score={result['score']:.4f}"
        )
        print(result["text"][:300])