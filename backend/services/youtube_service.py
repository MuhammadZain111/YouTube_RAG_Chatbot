from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """Extract a YouTube video ID from common URL formats."""

    from urllib.parse import urlparse, parse_qs

    parsed = urlparse(url)

    if parsed.hostname in {"youtu.be"}:
        return parsed.path.lstrip("/")

    if parsed.hostname in {
        "www.youtube.com",
        "youtube.com",
        "m.youtube.com"
    }:
        return parse_qs(parsed.query).get("v", [None])[0]

    raise ValueError("Invalid YouTube URL.")


def get_transcript(video_id: str) -> str:
    """Fetch a transcript and combine its text."""

    api = YouTubeTranscriptApi()

    transcript = api.fetch(video_id)

    return " ".join(
        snippet.text for snippet in transcript
    )