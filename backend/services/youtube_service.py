import os

from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
    YouTubeTranscriptApi,
)
from youtube_transcript_api._errors import (
    IpBlocked,
    RequestBlocked,
)
from youtube_transcript_api.proxies import WebshareProxyConfig
from dotenv import load_dotenv


load_dotenv()

username = os.getenv("WEBSHARE_PROXY_USERNAME")
password = os.getenv("WEBSHARE_PROXY_PASSWORD")


def extract_video_id(url: str) -> str:
    """Extract a YouTube video ID from common URL formats."""

    parsed = urlparse(url)

    if parsed.hostname in {"youtu.be"}:
        video_id = parsed.path.lstrip("/")
        if video_id:
            return video_id

    if parsed.hostname in {
        "www.youtube.com",
        "youtube.com",
        "m.youtube.com",
    }:
        if parsed.path.startswith("/shorts/") or parsed.path.startswith("/embed/"):
            video_id = parsed.path.split("/")[-1]
            if video_id:
                return video_id

        video_id = parse_qs(parsed.query).get("v", [None])[0]
        if video_id:
            return video_id

    raise ValueError("Invalid YouTube URL.")


def get_transcript(video_id: str) -> str:
    """Fetch a transcript and combine its text."""

    # if not username or not password:
    #     raise RuntimeError("Webshare proxy credentials are missing")

    # api = YouTubeTranscriptApi(
    #     proxy_config=WebshareProxyConfig(
    #         proxy_username=username,
    #         proxy_password=password,
    #     )
    # )

    api = YouTubeTranscriptApi();

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
    except (IpBlocked, RequestBlocked) as error:
        raise ValueError(
            "Transcript service is temporarily blocked. Please retry shortly."
        ) from error
    except Exception as error:
        raise ValueError(
            "Could not retrieve a transcript for this video. Please try again.", video_id
        ) from error

    text = " ".join(snippet.text for snippet in transcript)

    if not text.strip():
        raise ValueError(
            "This video has no caption text. Please choose a video with captions."
        )

    return text