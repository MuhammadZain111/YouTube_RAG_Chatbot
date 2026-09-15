import { Send } from "lucide-react";

export default function ChatInput({
  question,
  setQuestion,
  onSubmit,
  loading,
  disabled,
}) {
  function handleSubmit(event) {
    event.preventDefault();
    onSubmit();
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        value={question}
        onChange={(event) => setQuestion(event.target.value)}
        disabled={disabled || loading}
        placeholder="Ask a question about this video..."
        className="min-w-0 flex-1 rounded-xl border px-4 py-3 text-sm outline-none focus:border-blue-500 disabled:bg-slate-100"
      />

      <button
        type="submit"
        disabled={disabled || loading || !question.trim()}
        className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
      >
        <Send size={19} />
      </button>
    </form>
  );
}