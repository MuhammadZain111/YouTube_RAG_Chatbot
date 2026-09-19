import { useState } from "react";

import { askQuestion } from "../../services/api";
import ChatInput from "./ChatInput";
import MessageBubble from "./MessageBubble";

export default function ChatInterface({ videoId }) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit() {
    const submittedQuestion = question.trim();

    if (!videoId || !submittedQuestion || loading) {
      return;
    }

    setQuestion("");
    setError("");
    setMessages((currentMessages) => [
      ...currentMessages,
      { role: "user", content: submittedQuestion },
    ]);
    setLoading(true);

    try {
      const result = await askQuestion(videoId, submittedQuestion);
      setMessages((currentMessages) => [
        ...currentMessages,
        { role: "assistant", content: result.answer },
      ]);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="flex min-h-[28rem] flex-col rounded-2xl border bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-base font-semibold">Ask about the video</h2>

      <div className="mb-4 flex-1 space-y-3 overflow-y-auto rounded-xl bg-slate-50 p-3">
        {!videoId && (
          <p className="py-12 text-center text-sm text-slate-500">
            Load a video before asking a question.
          </p>
        )}

        {videoId && messages.length === 0 && (
          <p className="py-12 text-center text-sm text-slate-500">
            Ask your first question about this video.
          </p>
        )}

        {messages.map((message, index) => (
          <MessageBubble
            key={`${message.role}-${index}`}
            role={message.role}
            content={message.content}
          />
        ))}

        {loading && <MessageBubble role="assistant" content="Thinking..." />}
      </div>

      {error && <p className="mb-3 text-sm text-red-600">{error}</p>}

      <ChatInput
        question={question}
        setQuestion={setQuestion}
        onSubmit={handleSubmit}
        loading={loading}
        disabled={!videoId}
      />
    </section>
  );
}
