

from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
    YouTubeTranscriptApi,
)
from youtube_transcript_api.proxies import WebshareProxyConfig


# username = os.getenv("WEBSHARE_PROXY_USERNAME")
# password = os.getenv("WEBSHARE_PROXY_PASSWORD")





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

    # if not username or not password:
    #    raise RuntimeError("Webshare proxy credentials are missing")


    # api = YouTubeTranscriptApi(
    #     # proxy_config=WebshareProxyConfig(
    #     # proxy_username=username,
    #     # proxy_password=password,
    # )
    # )

    api = YouTubeTranscriptApi()


    try:
        transcript = api.fetch(video_id)

    except TranscriptsDisabled as error:
        raise ValueError(
            "This video has captions disabled. Please choose a video with captions."
        ) from error
    except NoTranscriptFound as error:
        raise ValueError(
            "This video does not have an available caption transcript. "
            "Please choose another video."
        ) from error
    except VideoUnavailable as error:
        raise ValueError(
            "This YouTube video is unavailable or private."
        ) from error

    text = " ".join(
        snippet.text for snippet in transcript
    )

    if not text.strip():
        raise ValueError(
            "This video has no caption text. Please choose a video with captions."
        )

    return text