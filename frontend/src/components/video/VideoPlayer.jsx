import { PlayCircle } from "lucide-react";

export default function VideoPlayer({ videoId, title }) {
  if (!videoId) {
    return (
      <div className="flex aspect-video items-center justify-center rounded-2xl bg-slate-900 text-center text-slate-400">
        <div>
          <PlayCircle className="mx-auto mb-3" size={42} />
          <p>Load a YouTube video to begin</p>
        </div>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-2xl bg-black">
      <iframe
        className="aspect-video w-full"
        src={`https://www.youtube.com/embed/${videoId}`}
        title={title || "YouTube Video"}
        allowFullScreen
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      />
    </div>
  );
}
