import { useState } from "react";

import VideoInput from "../components/video/VideoInput";
import VideoPlayer from "../components/video/VideoPlayer";
import VideoInfo from "../components/video/VideoInfo";
import ChatInterface from "../components/chat/ChatInterface";

export default function Home() {
  const [video, setVideo] = useState(null);

  function handleIndexed(result) {
    setVideo({
      videoId: result.video_id,
      chunks: result.chunks,
      title: result.title,
    });
  }

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold sm:text-3xl">
          YouTube AI Chatbot
        </h1>
        <p className="mt-2 text-sm text-slate-500">
          Paste a YouTube video and ask questions using LangChain.
        </p>
      </div>

      <VideoInput onIndexed={handleIndexed} />

      <div className="grid gap-6 lg:grid-cols-2">
        <div>
          <VideoPlayer
            videoId={video?.videoId}
            title={video?.title}
          />

          {video && (
            <VideoInfo
              videoId={video.videoId}
              title={video.title}
              chunks={video.chunks}
            />
          )}
        </div>

        <ChatInterface videoId={video?.videoId} />
      </div>
    </div>
  );
}