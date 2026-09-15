const API_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function indexVideo(youtubeUrl) {
  let response;

  try {
    response = await fetch(`${API_URL}/api/videos/index`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        youtube_url: youtubeUrl,
      }),
    });
  } catch {
    throw new Error(
      "Cannot connect to the backend. Start it with: cd backend && ./venv/bin/uvicorn main:app --reload"
    );
  }

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to index video.");
  }

  return data;
}

export async function askQuestion(videoId, question) {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      video_id: videoId,
      question,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to get answer.");
  }

  return data;
}