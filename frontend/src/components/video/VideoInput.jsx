import { useState } from "react";
import { Link, LoaderCircle } from "lucide-react";
import { indexVideo } from "../../services/api";

export default function VideoInput({ onIndexed }) {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    if (!url.trim()) {
      setError("Please enter a YouTube URL.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const result = await indexVideo(url);
      onIndexed(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-2xl border bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-base font-semibold">Load YouTube Video</h2>

      <form onSubmit={handleSubmit} className="flex flex-col gap-3 sm:flex-row">
        <input
          type="url"
          required
          value={url}
          onChange={(event) => setUrl(event.target.value)}
          placeholder="Paste YouTube video URL..."
          className="min-w-0 flex-1 rounded-xl border px-4 py-3 text-sm outline-none focus:border-blue-500"
        />

        <button
          type="submit"
          disabled={loading}
          className="flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-60"
        >
          {loading ? (
            <LoaderCircle className="animate-spin" size={18} />
          ) : (
            <Link size={18} />
          )}

          {loading ? "Indexing..." : "Load Video"}
        </button>
      </form>

      {error && (
        <p className="mt-3 rounded-lg bg-red-50 p-3 text-sm text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}
