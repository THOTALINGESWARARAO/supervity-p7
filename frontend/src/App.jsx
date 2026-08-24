import { useState } from "react";
import { askHR, runAgent } from "./services/api";
import "./index.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [conversationId] = useState(
    () => crypto.randomUUID()
  );
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState("agent");

  async function handleSubmit(event) {
    event.preventDefault();

    const question = input.trim();

    if (!question || loading) {
      return;
    }

    setInput("");

    setMessages((current) => [
      ...current,
      {
        role: "user",
        content: question,
      },
    ]);

    setLoading(true);

    try {
      const result =
        mode === "hr"
          ? await askHR(question, conversationId)
          : await runAgent(question);

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content:
            result.answer ??
            result.response ??
            "No response received.",
          sources: result.sources ?? [],
          action: result.action,
          result: result.result,
        },
      ]);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          role: "error",
          content:
            error.message ||
            "Unable to connect to the backend.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>HR Knowledge Assistant</h1>
          <p>
            Ask HR questions and manage your tasks using natural
            language.
          </p>
        </div>

        <div className="mode-switch">
          <button
            className={mode === "agent" ? "active" : ""}
            onClick={() => setMode("agent")}
            type="button"
          >
            Assistant
          </button>

          <button
            className={mode === "hr" ? "active" : ""}
            onClick={() => setMode("hr")}
            type="button"
          >
            Ask HR
          </button>
        </div>
      </header>

      <main className="chat-container">
        <section className="messages">
          {messages.length === 0 && (
            <div className="welcome">
              <h2>How can I help?</h2>

              <div className="examples">
                <button
                  type="button"
                  onClick={() =>
                    setInput("What is the leave policy?")
                  }
                >
                  What is the leave policy?
                </button>

                <button
                  type="button"
                  onClick={() =>
                    setInput("Create a task to complete onboarding")
                  }
                >
                  Create an onboarding task
                </button>

                <button
                  type="button"
                  onClick={() =>
                    setInput("Show my tasks")
                  }
                >
                  Show my tasks
                </button>
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <Message
              key={`${message.role}-${index}`}
              message={message}
            />
          ))}

          {loading && (
            <div className="message assistant">
              <div className="message-bubble loading">
                Thinking...
              </div>
            </div>
          )}
        </section>

        <form className="input-area" onSubmit={handleSubmit}>
          <input
            value={input}
            onChange={(event) =>
              setInput(event.target.value)
            }
            placeholder="Ask an HR question or manage a task..."
            disabled={loading}
          />

          <button
            type="submit"
            disabled={loading || !input.trim()}
          >
            Send
          </button>
        </form>
      </main>
    </div>
  );
}

function Message({ message }) {
  const isUser = message.role === "user";
  const isError = message.role === "error";

  return (
    <div
      className={`message ${
        isUser ? "user" : isError ? "error" : "assistant"
      }`}
    >
      <div className="message-label">
        {isUser ? "You" : isError ? "Error" : "Assistant"}
      </div>

      <div className="message-bubble">
        <div className="message-content">
          {message.content}
        </div>

        {message.sources?.length > 0 && (
          <div className="sources">
            <strong>Sources</strong>

            {message.sources.map((source, index) => (
              <div
                className="source"
                key={`${source.source}-${index}`}
              >
                <span>{source.source}</span>
                <small>
                  Chunk {source.chunk_index} · Score{" "}
                  {source.score}
                </small>
              </div>
            ))}
          </div>
        )}

        {message.action && (
          <div className="action">
            Action: <strong>{message.action}</strong>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;