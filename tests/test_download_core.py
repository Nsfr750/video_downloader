"""Tests for the download core module (options, playlists, history recording)."""

import os
import sys
from unittest.mock import MagicMock, Mock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import yt_dlp

from download_core import (
    PLAYLIST_TEMPLATE,
    VIDEO_TEMPLATE,
    build_ydl_options,
    download_url,
    entries_from_info,
)
from history import STATUS_COMPLETED, STATUS_FAILED
from main import VideoDownloader, is_yes

URL = "https://www.youtube.com/playlist?list=PL123"

VIDEO_INFO = {
    "id": "abc",
    "title": "My video",
    "webpage_url": "https://www.youtube.com/watch?v=abc",
    "requested_downloads": [{"filepath": "downloads/My video.mp4"}],
}

PLAYLIST_INFO = {
    "_type": "playlist",
    "title": "My playlist",
    "entries": [
        {
            "id": "a",
            "title": "First",
            "webpage_url": "https://www.youtube.com/watch?v=a",
            "requested_downloads": [
                {"filepath": "downloads/My playlist/001 - First.mp4"}
            ],
        },
        None,
        {
            "id": "c",
            "title": "Third",
            "webpage_url": "https://www.youtube.com/watch?v=c",
        },
    ],
}


def _youtube_dl(result=None, error=None) -> MagicMock:
    """Build a fake YoutubeDL class.

    Args:
        result: Value returned by extract_info
        error: Exception raised by extract_info instead of returning

    Returns:
        Mock usable in place of yt_dlp.YoutubeDL
    """
    youtube_dl = MagicMock()
    ydl = youtube_dl.return_value.__enter__.return_value
    if error is not None:
        ydl.extract_info.side_effect = error
    else:
        ydl.extract_info.return_value = result
    return youtube_dl


class TestBuildOptions:
    """Test cases for build_ydl_options."""

    def test_single_video_options(self):
        """Test that playlists are not downloaded by default."""
        options = build_ydl_options("downloads")

        assert options["noplaylist"] is True
        assert "ignoreerrors" not in options
        assert options["outtmpl"] == os.path.join("downloads", VIDEO_TEMPLATE)
        assert options["format"] == "best"
        assert "merge_output_format" not in options

    def test_playlist_options(self):
        """Test the options used to download an entire playlist."""
        options = build_ydl_options("downloads", playlist=True)

        assert options["noplaylist"] is False
        assert options["ignoreerrors"] is True
        assert options["outtmpl"] == os.path.join("downloads", PLAYLIST_TEMPLATE)

    def test_quality_format_and_hook(self):
        """Test that quality, format and progress hook are passed on."""
        hook = Mock()
        options = build_ydl_options("downloads", "720p", "mkv", progress_hook=hook)

        assert "height<=720" in options["format"]
        assert options["merge_output_format"] == "mkv"
        assert options["progress_hooks"] == [hook]

    @pytest.mark.parametrize("quiet", [True, False])
    def test_quiet(self, quiet):
        """Test that quiet mode also hides warnings."""
        options = build_ydl_options("downloads", quiet=quiet)

        assert options["quiet"] is quiet
        assert options["no_warnings"] is quiet

    def test_options_are_accepted_by_ytdlp(self, tmp_path):
        """Test that yt-dlp accepts the generated options."""
        for playlist in (False, True):
            options = build_ydl_options(str(tmp_path), playlist=playlist, quiet=True)
            with yt_dlp.YoutubeDL(options):
                pass


class TestOutputTemplate:
    """Test cases for the file names produced by the playlist template."""

    @pytest.fixture
    def ydl(self):
        """Create a YoutubeDL instance using the playlist template."""
        options = build_ydl_options("downloads", playlist=True, quiet=True)
        with yt_dlp.YoutubeDL(options) as ydl:
            yield ydl

    def test_single_video_is_not_put_in_a_folder(self, ydl):
        """Test that a plain video keeps the usual file name."""
        filename = ydl.prepare_filename({"id": "a", "title": "Video", "ext": "mp4"})

        assert os.path.normpath(filename) == os.path.join("downloads", "Video.mp4")

    def test_playlist_video_is_numbered_in_playlist_folder(self, ydl):
        """Test that playlist videos are numbered inside the playlist folder."""
        filename = ydl.prepare_filename(
            {
                "id": "a",
                "title": "Video",
                "ext": "mp4",
                "playlist_title": "My list",
                "playlist_index": 7,
            }
        )

        assert os.path.normpath(filename) == os.path.join(
            "downloads", "My list", "007 - Video.mp4"
        )


class TestEntriesFromInfo:
    """Test cases for entries_from_info."""

    def test_single_video(self):
        """Test the entry created for a single video."""
        entries = entries_from_info(VIDEO_INFO, URL, "720p", "mp4")

        assert len(entries) == 1
        entry = entries[0]
        assert entry.status == STATUS_COMPLETED
        assert entry.title == "My video"
        assert entry.url == "https://www.youtube.com/watch?v=abc"
        assert entry.file_path == "downloads/My video.mp4"
        assert entry.quality == "720p"
        assert entry.format == "mp4"
        assert entry.playlist == ""

    def test_video_without_page_url_uses_requested_url(self):
        """Test that the requested URL is used when yt-dlp gives none."""
        entries = entries_from_info({"title": "Video"}, URL)

        assert entries[0].url == URL
        assert entries[0].file_path == ""

    @pytest.mark.parametrize("info", [None, "text", Mock()])
    def test_no_result_is_a_failure(self, info):
        """Test that a missing result is reported as a failed download."""
        entries = entries_from_info(info, URL)

        assert len(entries) == 1
        assert entries[0].status == STATUS_FAILED
        assert entries[0].url == URL
        assert entries[0].error

    def test_playlist(self):
        """Test that a playlist gives one entry per video."""
        entries = entries_from_info(PLAYLIST_INFO, URL, "best", "auto")

        assert [entry.status for entry in entries] == [
            STATUS_COMPLETED,
            STATUS_FAILED,
            STATUS_COMPLETED,
        ]
        assert [entry.title for entry in entries] == ["First", "", "Third"]
        assert all(entry.playlist == "My playlist" for entry in entries)
        assert entries[0].url == "https://www.youtube.com/watch?v=a"
        assert entries[0].file_path == "downloads/My playlist/001 - First.mp4"
        assert entries[1].url == URL
        assert "2" in entries[1].error

    def test_empty_playlist_is_a_failure(self):
        """Test that a playlist without videos is reported as failed."""
        entries = entries_from_info(
            {"_type": "playlist", "title": "Empty", "entries": []}, URL
        )

        assert len(entries) == 1
        assert entries[0].status == STATUS_FAILED
        assert entries[0].playlist == "Empty"

    def test_nested_playlists(self):
        """Test that playlists inside a playlist (e.g. a channel) are flattened."""
        info = {
            "_type": "playlist",
            "title": "Channel",
            "entries": [
                {"_type": "playlist", "title": "Inner", "entries": [{"title": "A"}]},
                {"title": "B"},
            ],
        }

        entries = entries_from_info(info, URL)

        assert [(entry.title, entry.playlist) for entry in entries] == [
            ("A", "Inner"),
            ("B", "Channel"),
        ]


class TestDownloadUrl:
    """Test cases for download_url."""

    def test_download_records_history(self, isolated_history):
        """Test that a download is recorded in the history."""
        youtube_dl = _youtube_dl(VIDEO_INFO)
        options = build_ydl_options("downloads")

        entries = download_url(youtube_dl, URL, options, "720p", "mp4")

        youtube_dl.assert_called_once_with(options)
        ydl = youtube_dl.return_value.__enter__.return_value
        ydl.extract_info.assert_called_once_with(URL, download=True)
        assert [entry.title for entry in entries] == ["My video"]
        stored = isolated_history.get_entries()
        assert len(stored) == 1
        assert stored[0].title == "My video"
        assert stored[0].quality == "720p"
        assert stored[0].format == "mp4"

    def test_playlist_records_every_video(self, isolated_history):
        """Test that every video of a playlist is recorded."""
        entries = download_url(_youtube_dl(PLAYLIST_INFO), URL, {})

        assert len(entries) == 3
        stored = isolated_history.get_entries()
        assert [entry.title for entry in stored] == ["Third", "", "First"]
        assert sum(entry.completed for entry in stored) == 2

    def test_error_is_recorded_as_failed(self, isolated_history):
        """Test that a yt-dlp error becomes a failed history entry."""
        entries = download_url(
            _youtube_dl(error=Exception("Video unavailable")), URL, {}
        )

        assert len(entries) == 1
        assert entries[0].status == STATUS_FAILED
        assert entries[0].error == "Video unavailable"
        assert isolated_history.get_entries()[0].error == "Video unavailable"

    def test_history_write_error_does_not_fail_the_download(self, isolated_history):
        """Test that the download result is returned even if history fails."""
        with patch.object(
            isolated_history, "add_many", side_effect=OSError("disk full")
        ):
            entries = download_url(_youtube_dl(VIDEO_INFO), URL, {})

        assert entries[0].completed is True


class TestVideoDownloaderPlaylist:
    """Test cases for playlist support in the CLI downloader."""

    @pytest.fixture
    def downloader(self, tmp_path):
        """Create a VideoDownloader writing to a temporary directory."""
        return VideoDownloader(download_dir=str(tmp_path / "downloads"))

    def test_playlist_disabled_by_default(self, downloader):
        """Test that playlists are not downloaded by default."""
        assert downloader.playlist is False

    @patch("main.yt_dlp.YoutubeDL")
    def test_single_video_mode(self, mock_ydl, downloader):
        """Test that only one video is requested when playlists are off."""
        mock_ydl.return_value.__enter__.return_value.extract_info.return_value = (
            VIDEO_INFO
        )

        assert downloader.download_video(URL) is True
        assert mock_ydl.call_args.args[0]["noplaylist"] is True

    @patch("main.yt_dlp.YoutubeDL")
    def test_playlist_mode(self, mock_ydl, downloader, isolated_history):
        """Test that an entire playlist is downloaded and recorded."""
        mock_ydl.return_value.__enter__.return_value.extract_info.return_value = (
            PLAYLIST_INFO
        )
        downloader.playlist = True

        assert downloader.download_video(URL) is True
        options = mock_ydl.call_args.args[0]
        assert options["noplaylist"] is False
        assert options["ignoreerrors"] is True
        assert len(downloader.last_entries) == 3
        assert len(isolated_history) == 3

    @patch("main.yt_dlp.YoutubeDL")
    def test_playlist_with_no_downloaded_video_fails(self, mock_ydl, downloader):
        """Test that a playlist where every video failed is a failure."""
        mock_ydl.return_value.__enter__.return_value.extract_info.return_value = {
            "_type": "playlist",
            "title": "Broken",
            "entries": [None, None],
        }
        downloader.playlist = True

        assert downloader.download_video(URL) is False

    @patch("main.yt_dlp.YoutubeDL")
    def test_summary_counts_playlist_videos(self, mock_ydl, downloader, capsys):
        """Test that the summary counts videos, not URLs."""
        mock_ydl.return_value.__enter__.return_value.extract_info.return_value = (
            PLAYLIST_INFO
        )
        downloader.playlist = True

        downloader.download_videos([URL])

        output = capsys.readouterr().out
        assert "Successful: 2" in output
        assert "Failed: 1" in output
        assert "Total: 3" in output

    @pytest.mark.parametrize(
        "answer, expected",
        [
            ("y", True),
            ("Y", True),
            ("yes", True),
            ("", False),
            ("n", False),
            ("x", False),
        ],
    )
    def test_select_playlist(self, downloader, english, answer, expected):
        """Test the playlist question of the download menu."""
        with patch("builtins.input", return_value=answer):
            assert downloader.select_playlist() is expected


class TestIsYes:
    """Test cases for is_yes."""

    @pytest.mark.parametrize(
        "language, answer",
        [
            ("it", "s"),
            ("it", "Sì"),
            ("es", "sí"),
            ("fr", "oui"),
            ("de", "ja"),
            ("de", "y"),
        ],
    )
    def test_localized_yes(self, language, answer):
        """Test that the translated "yes" is accepted."""
        from lang import get_language_manager

        manager = get_language_manager()
        previous = manager.get_language()
        manager.set_language(language)
        try:
            assert is_yes(answer) is True
        finally:
            manager.set_language(previous)

    @pytest.mark.parametrize("answer", ["", "  ", "n", "no", "0"])
    def test_no(self, english, answer):
        """Test that anything else is not a yes."""
        assert is_yes(answer) is False
