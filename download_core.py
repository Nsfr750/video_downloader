"""Download core for Video Downloader application.

This module contains the yt-dlp logic shared by the CLI and the GUI:
quality/format options, playlist handling and download history recording.
"""

import os
from typing import Any, Callable, Dict, List, Optional

from history import STATUS_FAILED, HistoryEntry, get_history
from logger import get_logger

# Quality options mapping
QUALITY_OPTIONS = {
    "best": "best",
    "worst": "worst",
    "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
    "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
    "audio": "bestaudio/best",
}

# Format options mapping
FORMAT_OPTIONS = {
    "auto": None,  # Keep original format
    "mp4": "mp4",
    "webm": "webm",
    "mkv": "mkv",
    "avi": "avi",
    "mp3": "mp3",  # Audio only
    "m4a": "m4a",  # Audio only
    "wav": "wav",  # Audio only
}

# Output file name of a single video
VIDEO_TEMPLATE = "%(title)s.%(ext)s"

# Output file name with playlists enabled: videos of a playlist go into a
# folder named after it and are numbered; a single video is saved as usual
PLAYLIST_TEMPLATE = os.path.join(
    "%(playlist_title|)s", "%(playlist_index&{:03d} - |)s%(title)s.%(ext)s"
)


def build_ydl_options(
    download_dir: str,
    quality: str = "best",
    output_format: str = "auto",
    playlist: bool = False,
    progress_hook: Optional[Callable[[dict], None]] = None,
    quiet: bool = False,
) -> Dict[str, Any]:
    """Build the yt-dlp options for a download.

    Args:
        download_dir: Directory to save downloaded videos
        quality: Video quality (best, worst, 1080p, 720p, 480p, 360p, audio)
        output_format: Output format (auto, mp4, webm, mkv, avi, mp3, m4a, wav)
        playlist: Download every video of a playlist URL instead of one video
        progress_hook: Function called by yt-dlp with the download progress
        quiet: Hide yt-dlp console output and warnings

    Returns:
        Options dictionary for yt_dlp.YoutubeDL
    """
    template = PLAYLIST_TEMPLATE if playlist else VIDEO_TEMPLATE
    options: Dict[str, Any] = {
        "format": QUALITY_OPTIONS.get(quality, "best"),
        "outtmpl": os.path.join(download_dir, template),
        "quiet": quiet,
        "no_warnings": quiet,
        "noplaylist": not playlist,
        "progress_hooks": [progress_hook] if progress_hook else [],
    }

    # One unavailable video must not stop the rest of the playlist
    if playlist:
        options["ignoreerrors"] = True

    # Add format conversion if specified
    if output_format != "auto":
        options["merge_output_format"] = FORMAT_OPTIONS.get(output_format)

    return options


def _file_path(info: Dict[str, Any]) -> str:
    """Get the path of the file written by yt-dlp for a video.

    Args:
        info: yt-dlp information dictionary of a video

    Returns:
        File path, or an empty string if unknown
    """
    downloads = info.get("requested_downloads") or []
    if downloads and isinstance(downloads[0], dict):
        return downloads[0].get("filepath") or ""
    return info.get("filepath") or ""


def entries_from_info(
    info: Any, url: str, quality: str = "best", output_format: str = "auto"
) -> List[HistoryEntry]:
    """Convert the result of a yt-dlp download into history entries.

    A playlist gives one entry per video; videos that could not be downloaded
    are returned as failed entries.

    Args:
        info: Value returned by YoutubeDL.extract_info
        url: URL that was requested
        quality: Quality used for the download
        output_format: Output format used for the download

    Returns:
        List of history entries, never empty
    """

    def failed(error: str, playlist: str = "") -> HistoryEntry:
        return HistoryEntry(
            url=url,
            status=STATUS_FAILED,
            quality=quality,
            format=output_format,
            playlist=playlist,
            error=error,
        )

    if not isinstance(info, dict):
        return [failed("No video downloaded")]

    if info.get("_type") != "playlist" and "entries" not in info:
        return [
            HistoryEntry(
                url=info.get("webpage_url") or info.get("original_url") or url,
                title=info.get("title") or "",
                quality=quality,
                format=output_format,
                file_path=_file_path(info),
                playlist=info.get("playlist_title") or "",
            )
        ]

    playlist_title = info.get("title") or ""
    entries: List[HistoryEntry] = []
    for index, item in enumerate(info.get("entries") or [], 1):
        if isinstance(item, dict):
            item.setdefault("playlist_title", playlist_title)
            entries.extend(entries_from_info(item, url, quality, output_format))
        else:
            entries.append(
                failed(f"Playlist item {index} not downloaded", playlist_title)
            )

    return entries or [failed("Empty playlist", playlist_title)]


def download_url(
    youtube_dl: Callable[[Dict[str, Any]], Any],
    url: str,
    options: Dict[str, Any],
    quality: str = "best",
    output_format: str = "auto",
) -> List[HistoryEntry]:
    """Download a URL with yt-dlp and record the result in the history.

    Args:
        youtube_dl: The yt_dlp.YoutubeDL class
        url: URL of the video or playlist to download
        options: Options built by build_ydl_options
        quality: Quality used for the download (stored in the history)
        output_format: Output format used for the download (stored in the history)

    Returns:
        One history entry per video, completed or failed; never empty
    """
    try:
        with youtube_dl(options) as ydl:
            info = ydl.extract_info(url, download=True)
        entries = entries_from_info(info, url, quality, output_format)
    except Exception as e:
        entries = [
            HistoryEntry(
                url=url,
                status=STATUS_FAILED,
                quality=quality,
                format=output_format,
                error=str(e),
            )
        ]

    try:
        get_history().add_many(entries)
    except OSError as e:
        get_logger().warning(f"Could not save download history: {e}")

    return entries
