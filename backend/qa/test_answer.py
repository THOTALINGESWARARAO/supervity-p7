from backend.qa.answer import answer_question


def main():
    question = "What is the company's policy on cryptocurrency investments?"

    result = answer_question(question)

    print("\nQUESTION:")
    print(question)

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")

    for source in result["sources"]:
        print(
            f"- {source['source']} "
            f"(chunk={source['chunk_index']}, "
            f"score={source['score']})"
        )


if __name__ == "__main__":
    main()