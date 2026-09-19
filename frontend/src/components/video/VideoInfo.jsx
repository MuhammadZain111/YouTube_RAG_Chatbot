export default function VideoInfo({ title, videoId, chunks }) {
  return (
    <div className="mt-4 rounded-xl border bg-white p-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h2 className="font-semibold">{title || "YouTube Video"}</h2>

        <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-medium text-green-700">
          Video Indexed
        </span>
      </div>

      <p className="mt-2 text-sm text-slate-500">Video ID: {videoId}</p>

      {chunks !== undefined && (
        <p className="mt-1 text-xs text-slate-400">
          Transcript chunks: {chunks}
        </p>
      )}
    </div>
  );
}
