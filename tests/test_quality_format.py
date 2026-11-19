"""Tests for quality selection and format conversion options."""

import os
import sys
from unittest.mock import Mock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lang import get_language_manager
from lang.translations import TRANSLATIONS
from main import VideoDownloader

QUALITY_CHOICES = [
    ("1", "best"),
    ("2", "worst"),
    ("3", "1080p"),
    ("4", "720p"),
    ("5", "480p"),
    ("6", "360p"),
    ("7", "audio"),
]

FORMAT_CHOICES = [
    ("1", "auto"),
    ("2", "mp4"),
    ("3", "webm"),
    ("4", "mkv"),
    ("5", "avi"),
    ("6", "mp3"),
    ("7", "m4a"),
    ("8", "wav"),
]


@pytest.fixture
def downloader(tmp_path):
    """Create a VideoDownloader instance writing to a temporary directory."""
    return VideoDownloader(download_dir=str(tmp_path / "downloads"))


@pytest.fixture
def english():
    """Force the English language for the duration of a test."""
    manager = get_language_manager()
    previous = manager.get_language()
    manager.set_language("en")
    yield manager
    manager.set_language(previous)


def _ydl_options(mock_ydl) -> dict:
    """Return the options dictionary passed to the mocked YoutubeDL."""
    return mock_ydl.call_args.args[0]


class TestQualitySelection:
    """Test cases for video quality selection."""

    def test_default_quality(self, downloader):
        """Test that the default quality is 'best'."""
        assert downloader.quality == "best"

    def test_init_with_quality(self, tmp_path):
        """Test that the quality passed to the constructor is stored."""
        downloader = VideoDownloader(download_dir=str(tmp_path), quality="720p")
        assert downloader.quality == "720p"

    @pytest.mark.parametrize("choice, expected", QUALITY_CHOICES)
    def test_select_quality(self, downloader, choice, expected):
        """Test that each menu choice maps to the right quality."""
        with patch("builtins.input", return_value=choice):
            assert downloader.select_quality() == expected

    def test_select_quality_default(self, downloader):
        """Test that an empty answer selects the best quality."""
        with patch("builtins.input", return_value=""):
            assert downloader.select_quality() == "best"

    def test_select_quality_invalid_then_valid(self, downloader, english, capsys):
        """Test that an invalid choice is rejected and asked again."""
        with patch("builtins.input", side_effect=["9", "abc", "4"]) as mock_input:
            assert downloader.select_quality() == "720p"
        assert mock_input.call_count == 3
        assert "Invalid choice" in capsys.readouterr().out

    def test_every_menu_quality_has_a_format_string(self):
        """Test that every selectable quality is known to yt-dlp options."""
        for _choice, quality in QUALITY_CHOICES:
            assert quality in VideoDownloader.QUALITY_OPTIONS

    @pytest.mark.parametrize("quality", ["1080p", "720p", "480p", "360p"])
    def test_resolution_is_limited(self, quality):
        """Test that resolution qualities cap the video height."""
        height = quality.rstrip("p")
        assert f"height<={height}" in VideoDownloader.QUALITY_OPTIONS[quality]

    @pytest.mark.parametrize("quality", [q for _c, q in QUALITY_CHOICES])
    @patch("main.yt_dlp.YoutubeDL")
    def test_download_uses_selected_quality(self, mock_ydl, downloader, quality):
        """Test that the selected quality is passed to yt-dlp."""
        mock_ydl.return_value.__enter__.return_value = Mock()
        downloader.quality = quality

        assert downloader.download_video("https://youtube.com/test") is True
        assert (
            _ydl_options(mock_ydl)["format"]
            == VideoDownloader.QUALITY_OPTIONS[quality]
        )

    @patch("main.yt_dlp.YoutubeDL")
    def test_download_unknown_quality_falls_back_to_best(self, mock_ydl, downloader):
        """Test that an unknown quality falls back to 'best'."""
        mock_ydl.return_value.__enter__.return_value = Mock()
        downloader.quality = "4320p"

        downloader.download_video("https://youtube.com/test")
        assert _ydl_options(mock_ydl)["format"] == "best"


class TestFormatSelection:
    """Test cases for output format selection."""

    def test_default_format(self, downloader):
        """Test that the default format keeps the original one."""
        assert downloader.format == "auto"

    def test_init_with_format(self, tmp_path):
        """Test that the format passed to the constructor is stored."""
        downloader = VideoDownloader(download_dir=str(tmp_path), format="mkv")
        assert downloader.format == "mkv"

    @pytest.mark.parametrize("choice, expected", FORMAT_CHOICES)
    def test_select_format(self, downloader, choice, expected):
        """Test that each menu choice maps to the right format."""
        with patch("builtins.input", return_value=choice):
            assert downloader.select_format() == expected

    def test_select_format_default(self, downloader):
        """Test that an empty answer keeps the original format."""
        with patch("builtins.input", return_value=""):
            assert downloader.select_format() == "auto"

    def test_select_format_invalid_then_valid(self, downloader, english, capsys):
        """Test that an invalid choice is rejected and asked again."""
        with patch("builtins.input", side_effect=["0", "9", "2"]) as mock_input:
            assert downloader.select_format() == "mp4"
        assert mock_input.call_count == 3
        assert "Invalid choice" in capsys.readouterr().out

    def test_every_menu_format_is_known(self):
        """Test that every selectable format is in the format options."""
        for _choice, output_format in FORMAT_CHOICES:
            assert output_format in VideoDownloader.FORMAT_OPTIONS

    @patch("main.yt_dlp.YoutubeDL")
    def test_download_auto_format_does_not_convert(self, mock_ydl, downloader):
        """Test that the 'auto' format does not request a conversion."""
        mock_ydl.return_value.__enter__.return_value = Mock()

        downloader.download_video("https://youtube.com/test")
        assert "merge_output_format" not in _ydl_options(mock_ydl)

    @pytest.mark.parametrize(
        "output_format", [f for _c, f in FORMAT_CHOICES if f != "auto"]
    )
    @patch("main.yt_dlp.YoutubeDL")
    def test_download_uses_selected_format(self, mock_ydl, downloader, output_format):
        """Test that the selected format is passed to yt-dlp."""
        mock_ydl.return_value.__enter__.return_value = Mock()
        downloader.format = output_format

        assert downloader.download_video("https://youtube.com/test") is True
        assert _ydl_options(mock_ydl)["merge_output_format"] == output_format


class TestDownloadMenu:
    """Test cases for the quality and format prompts in the download menu."""

    @patch("main.yt_dlp.YoutubeDL")
    def test_download_menu_applies_quality_and_format(self, mock_ydl, tmp_path):
        """Test that the menu choices reach the yt-dlp options."""
        from menu import Menu

        mock_ydl.return_value.__enter__.return_value = Mock()
        answers = ["4", "2", "https://youtube.com/test", ""]

        with patch("builtins.input", side_effect=answers), patch(
            "main.VideoDownloader.__init__.__defaults__",
            (str(tmp_path / "downloads"), "best", "auto"),
        ):
            Menu().download_menu()

        options = _ydl_options(mock_ydl)
        assert options["format"] == VideoDownloader.QUALITY_OPTIONS["720p"]
        assert options["merge_output_format"] == "mp4"


class TestTranslations:
    """Test cases for the translation strings of the new options."""

    NEW_KEYS = [
        "quality_title",
        "quality_select",
        "quality_best",
        "quality_worst",
        "quality_audio",
        "quality_default",
        "quality_invalid",
        "format_title",
        "format_select",
        "format_auto",
        "format_default",
        "format_invalid",
        "paypal_label",
        "monero_label",
        "qr_error_load",
        "qr_error_generate",
        "qr_unavailable",
    ]

    @pytest.mark.parametrize("language", sorted(TRANSLATIONS))
    def test_new_keys_are_translated(self, language):
        """Test that every language defines the new strings."""
        missing = [key for key in self.NEW_KEYS if key not in TRANSLATIONS[language]]
        assert missing == []

    @pytest.mark.parametrize("language", sorted(set(TRANSLATIONS) - {"en"}))
    def test_all_languages_have_the_same_keys(self, language):
        """Test that no language is missing a string defined in English."""
        assert set(TRANSLATIONS[language]) == set(TRANSLATIONS["en"])

    @pytest.mark.parametrize("language", sorted(set(TRANSLATIONS) - {"en"}))
    def test_titles_are_not_left_in_english(self, language):
        """Test that the selection titles are really translated."""
        for key in ("quality_title", "quality_select", "format_title", "format_select"):
            assert TRANSLATIONS[language][key] != TRANSLATIONS["en"][key]
