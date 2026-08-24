import json
import os

from dotenv import load_dotenv
from groq import Groq

from backend.agent.tools import (
    create_task,
    list_tasks,
    search_hr_documents,
    update_task,
)


load_dotenv(override=True)

GROQ_MODEL = "openai/gpt-oss-20b"


class HRAgent:
    """LLM-powered agent that routes requests to application tools."""

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.client = Groq(api_key=api_key)

    def _build_router_prompt(self, message: str) -> str:
        """Build a structured intent-routing prompt."""

        return f"""
You are an HR assistant intent router.

Determine which application action should handle the user's request.

Allowed actions:

1. search_hr_documents
   Use for questions about HR policies, benefits, procedures,
   employee handbook information, IT setup, security policies,
   leave, insurance, onboarding information, or other HR
   knowledge-base content.

2. create_task
   Use when the user wants to create a new task.

3. list_tasks
   Use when the user wants to see, list, or retrieve their tasks.

4. update_task
   Use when the user wants to modify an existing task.

5. none
   Use when the request does not match any supported action.

Return ONLY valid JSON.

For search_hr_documents:

{{
  "action": "search_hr_documents",
  "arguments": {{
    "query": "search query"
  }}
}}

For create_task:

{{
  "action": "create_task",
  "arguments": {{
    "title": "task title",
    "description": "optional description",
    "priority": "low|medium|high",
    "due_date": "optional date"
  }}
}}

For list_tasks:

{{
  "action": "list_tasks",
  "arguments": {{}}
}}

For update_task:

{{
  "action": "update_task",
  "arguments": {{
    "task_id": "task UUID",
    "title": "optional title",
    "description": "optional description",
    "status": "todo|in_progress|completed",
    "priority": "low|medium|high",
    "due_date": "optional date"
  }}
}}

For unsupported requests:

{{
  "action": "none",
  "arguments": {{}}
}}

Do not invent task IDs.

USER REQUEST:
{message}
""".strip()

    def _route(self, message: str) -> dict:
        """Use the LLM to determine the requested action."""

        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise JSON intent router."
                    ),
                },
                {
                    "role": "user",
                    "content": self._build_router_prompt(
                        message
                    ),
                },
            ],
            temperature=0,
        )

        content = (
            response.choices[0].message.content or ""
        ).strip()

        try:
            result = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Agent returned invalid JSON."
            ) from exc

        if not isinstance(result, dict):
            raise ValueError(
                "Agent response must be a JSON object."
            )

        return result

    def _execute_action(
        self,
        action: str,
        arguments: dict,
    ):
        """Execute the application tool selected by the agent."""

        if action == "search_hr_documents":
            return search_hr_documents(**arguments)

        if action == "create_task":
            return create_task(**arguments)

        if action == "list_tasks":
            return list_tasks()

        if action == "update_task":
            return update_task(**arguments)

        if action == "none":
            return None

        raise ValueError(
            f"Unsupported agent action: {action}"
        )

    def _build_response(
        self,
        message: str,
        action: str,
        result,
    ) -> str:
        """Generate a natural-language response from tool output."""

        if action == "none":
            return (
                "I can help with HR knowledge-base questions "
                "and task management."
            )

        # Listing tasks is deterministic and does not require
        # another LLM call. This also avoids unnecessary Groq
        # token consumption and rate-limit failures.
        if action == "list_tasks":
            if not result:
                return "You have no tasks."

            lines = ["Your tasks:"]

            for task in result:
                lines.append(
                    f"- {task.get('title', 'Untitled')} "
                    f"(status: {task.get('status', 'unknown')}, "
                    f"priority: {task.get('priority', 'unknown')})"
                )

            return "\n".join(lines)

        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a concise and professional "
                        "HR assistant. Summarize the application "
                        "result accurately. Do not invent information."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"USER REQUEST:\n{message}\n\n"
                        f"ACTION:\n{action}\n\n"
                        f"APPLICATION RESULT:\n"
                        f"{json.dumps(result, default=str)}"
                    ),
                },
            ],
            temperature=0,
        )

        return (
            response.choices[0].message.content or ""
        ).strip()

    def run(self, message: str) -> dict:
        """Route a request, execute the selected tool, and respond."""

        if not message.strip():
            raise ValueError(
                "Message must not be empty."
            )

        route = self._route(message)

        action = route.get("action")
        arguments = route.get("arguments", {})

        if not isinstance(arguments, dict):
            raise ValueError(
                "Agent arguments must be a JSON object."
            )

        result = self._execute_action(
            action=action,
            arguments=arguments,
        )

        response = self._build_response(
            message=message,
            action=action,
            result=result,
        )

        return {
            "response": response,
            "action": action,
            "arguments": arguments,
            "result": result,
        }


agent = HRAgent()


def run_agent(message: str) -> dict:
    """Convenience function for running the HR agent."""

    return agent.run(message)