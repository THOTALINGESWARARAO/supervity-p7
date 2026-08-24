import os

from dotenv import load_dotenv
from groq import Groq

from backend.ingestion.retrieve import search


load_dotenv()


GROQ_MODEL = "groq/compound-mini"

DEFAULT_TOP_K = 3
DEFAULT_SCORE_THRESHOLD = 0.30


class HRQuestionAnswering:
    """Generate grounded HR answers using RAG retrieval and Groq."""

    def __init__(
        self,
        top_k: int = DEFAULT_TOP_K,
        score_threshold: float = DEFAULT_SCORE_THRESHOLD,
    ):
        self.top_k = top_k
        self.score_threshold = score_threshold

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.client = Groq(api_key=api_key)

    def retrieve_context(self, question: str) -> list[dict]:
        """Retrieve relevant HR document chunks."""

        return search(
            query=question,
            top_k=self.top_k,
            score_threshold=self.score_threshold,
        )

    def build_context(self, results: list[dict]) -> str:
        """Build the context supplied to the LLM."""

        context_parts = []

        for result in results:
            context_parts.append(
                f"""
Source: {result["source"]}
Chunk: {result["chunk_index"]}
Similarity Score: {result["score"]:.4f}

Content:
{result["text"]}
""".strip()
            )

        return "\n\n---\n\n".join(context_parts)

    def build_prompt(
        self,
        question: str,
        context: str,
        conversation_context: str = "",
    ) -> str:
        """Build a grounded HR question-answering prompt."""

        conversation_section = ""

        if conversation_context.strip():
            conversation_section = f"""

RECENT CONVERSATION:
{conversation_context}
""".strip()

        return f"""
You are an HR assistant for the company.

Answer the user's question using ONLY the HR knowledge base
context provided below.

The recent conversation is provided only to understand references
such as "that", "it", "they", or follow-up questions. Do not treat
conversation history as authoritative HR policy.

Rules:
1. Use only the provided HR context for HR facts.
2. Use recent conversation only to understand conversational context.
3. Do not use outside knowledge.
4. Do not invent, assume, or infer HR policies that are not
   explicitly supported by the HR context.
5. If the HR context does not contain enough information to answer
   the question, say:
   "I could not find this information in the HR knowledge base."
6. Give a concise, clear, and professional answer.
7. When useful, mention the relevant HR document.

HR KNOWLEDGE BASE CONTEXT:
{context}

{conversation_section}

USER QUESTION:
{question}
""".strip()

    def generate_answer(
        self,
        question: str,
        context: str,
        conversation_context: str = "",
    ) -> str:
        """Generate an answer using Groq."""

        prompt = self.build_prompt(
            question=question,
            context=context,
            conversation_context=conversation_context,
        )

        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise and grounded HR "
                        "question-answering assistant."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
        )

        return response.choices[0].message.content.strip()

    def answer(
        self,
        question: str,
        conversation_context: str = "",
    ) -> dict:
        """Retrieve context and generate a grounded HR answer."""

        if not question.strip():
            raise ValueError("Question must not be empty.")

        results = self.retrieve_context(question)

        if not results:
            return {
                "answer": (
                    "I could not find this information in "
                    "the HR knowledge base."
                ),
                "sources": [],
            }

        context = self.build_context(results)

        answer = self.generate_answer(
            question=question,
            context=context,
            conversation_context=conversation_context,
        )

        sources = [
            {
                "source": result["source"],
                "chunk_index": result["chunk_index"],
                "score": round(result["score"], 4),
            }
            for result in results
        ]

        return {
            "answer": answer,
            "sources": sources,
        }


qa = HRQuestionAnswering()


def answer_question(
    question: str,
    conversation_context: str = "",
) -> dict:
    """Convenience function for answering an HR question."""

    return qa.answer(
        question=question,
        conversation_context=conversation_context,
    )