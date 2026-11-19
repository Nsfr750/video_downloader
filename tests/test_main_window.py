"""Tests for the quality, format and sponsor features of the GUI."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

pytest.importorskip("PySide6")

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QLabel

from lang.translations import TRANSLATIONS
from main import VideoDownloader
from ui import main_window
from ui.main_window import DownloadThread, MainWindow

QUALITIES = ["best", "worst", "1080p", "720p", "480p", "360p", "audio"]
FORMATS = ["auto", "mp4", "webm", "mkv", "avi", "mp3", "m4a", "wav"]


@pytest.fixture(scope="module")
def app():
    """Provide the QApplication shared by the GUI tests."""
    return QApplication.instance() or QApplication([])


@pytest.fixture
def window(app):
    """Create a MainWindow in English and restore the language afterwards."""
    window = MainWindow()
    previous = window.lang_manager.get_language()
    window.lang_manager.set_language("en")
    window._update_language()
    yield window
    window.lang_manager.set_language(previous)
    window.download_thread = None  # avoid the "download running" prompt on close
    window.close()


def _combo_data(combo) -> list:
    """Return the data values of all the items of a combo box."""
    return [combo.itemData(index) for index in range(combo.count())]


class TestOptionsMapping:
    """Test cases for the yt-dlp option tables used by the GUI."""

    def test_quality_options_match_cli(self):
        """Test that GUI and CLI use the same quality format strings."""
        assert main_window.QUALITY_OPTIONS == VideoDownloader.QUALITY_OPTIONS

    def test_format_options_match_cli(self):
        """Test that GUI and CLI offer the same output formats."""
        assert main_window.FORMAT_OPTIONS == VideoDownloader.FORMAT_OPTIONS


class TestQualityFormatWidgets:
    """Test cases for the quality and format selectors."""

    def test_defaults(self, window):
        """Test the default quality and format."""
        assert window.quality == "best"
        assert window.format == "auto"
        assert window.quality_combo.currentData() == "best"
        assert window.format_combo.currentData() == "auto"

    def test_combo_items(self, window):
        """Test that the selectors list every quality and format."""
        assert _combo_data(window.quality_combo) == QUALITIES
        assert _combo_data(window.format_combo) == FORMATS

    def test_quality_change(self, window):
        """Test that choosing a quality updates the window state."""
        window.quality_combo.setCurrentIndex(window.quality_combo.findData("720p"))
        assert window.quality == "720p"

    def test_format_change(self, window):
        """Test that choosing a format updates the window state."""
        window.format_combo.setCurrentIndex(window.format_combo.findData("mkv"))
        assert window.format == "mkv"

    def test_start_download_passes_quality_and_format(self, window):
        """Test that the download thread receives the selected options."""
        window.quality_combo.setCurrentIndex(window.quality_combo.findData("480p"))
        window.format_combo.setCurrentIndex(window.format_combo.findData("webm"))
        window.urls = ["https://youtube.com/test"]

        with patch("ui.main_window.DownloadThread") as mock_thread:
            window._start_download()

        mock_thread.assert_called_once_with(
            ["https://youtube.com/test"], window.download_dir, "480p", "webm"
        )
        mock_thread.return_value.start.assert_called_once()


class TestLanguageChange:
    """Test cases for the translation of the quality and format selectors."""

    @pytest.mark.parametrize("language", sorted(set(TRANSLATIONS) - {"en"}))
    def test_titles_and_labels_are_translated(self, window, language):
        """Test that group titles and labels follow the selected language."""
        strings = TRANSLATIONS[language]
        window.lang_manager.set_language(language)
        window._update_language()

        assert window.quality_group.title() == strings["quality_title"]
        assert window.quality_label.text() == strings["quality_select"]
        assert window.format_group.title() == strings["format_title"]
        assert window.format_label.text() == strings["format_select"]

    @pytest.mark.parametrize("language", sorted(set(TRANSLATIONS) - {"en"}))
    def test_combo_items_are_translated(self, window, language):
        """Test that the selector items follow the selected language."""
        strings = TRANSLATIONS[language]
        window.lang_manager.set_language(language)
        window._update_language()

        assert window.quality_combo.itemText(0) == strings["quality_best"]
        assert window.quality_combo.itemText(1) == strings["quality_worst"]
        assert window.quality_combo.itemText(6) == strings["quality_audio"]
        assert window.format_combo.itemText(0) == strings["format_auto"]
        assert _combo_data(window.quality_combo) == QUALITIES
        assert _combo_data(window.format_combo) == FORMATS

    def test_selection_is_kept_after_language_change(self, window):
        """Test that changing language does not reset the selected options."""
        window.quality_combo.setCurrentIndex(window.quality_combo.findData("720p"))
        window.format_combo.setCurrentIndex(window.format_combo.findData("mp3"))

        window.lang_manager.set_language("it")
        window._update_language()

        assert window.quality_combo.currentData() == "720p"
        assert window.format_combo.currentData() == "mp3"
        assert window.quality == "720p"
        assert window.format == "mp3"


class TestDownloadThread:
    """Test cases for the quality and format handling of the download thread."""

    def _run(self, quality: str, output_format: str) -> dict:
        """Run a download thread synchronously with a mocked yt-dlp.

        Args:
            quality: Quality passed to the thread
            output_format: Output format passed to the thread

        Returns:
            Options dictionary passed to YoutubeDL
        """
        thread = DownloadThread(
            ["https://youtube.com/test"], "downloads", quality, output_format
        )
        thread.yt_dlp = MagicMock()
        thread.run()
        return thread.yt_dlp.YoutubeDL.call_args.args[0]

    def test_defaults(self, app):
        """Test the default quality and format of the thread."""
        thread = DownloadThread([], "downloads")
        assert thread.quality == "best"
        assert thread.format == "auto"

    @pytest.mark.parametrize("quality", QUALITIES)
    def test_quality_is_passed_to_ytdlp(self, app, quality):
        """Test that the selected quality reaches yt-dlp."""
        options = self._run(quality, "auto")

        assert options["format"] == main_window.QUALITY_OPTIONS[quality]
        assert "merge_output_format" not in options

    @pytest.mark.parametrize("output_format", [f for f in FORMATS if f != "auto"])
    def test_format_is_passed_to_ytdlp(self, app, output_format):
        """Test that the selected output format reaches yt-dlp."""
        options = self._run("best", output_format)

        assert options["merge_output_format"] == output_format

    def test_finished_signal_counts_results(self, app):
        """Test that successful and failed downloads are counted."""
        thread = DownloadThread(["https://a.test", "https://b.test"], "downloads")
        thread.yt_dlp = MagicMock()
        ydl = thread.yt_dlp.YoutubeDL.return_value.__enter__.return_value
        ydl.download.side_effect = [None, Exception("failed")]
        results = []
        thread.download_finished.connect(lambda ok, ko: results.append((ok, ko)))

        thread.run()

        assert results == [(1, 1)]


class TestSponsorDialog:
    """Test cases for the sponsor dialog."""

    def _open(self, app, window) -> dict:
        """Open the sponsor dialog, inspect it and close it.

        Args:
            app: QApplication instance
            window: MainWindow under test

        Returns:
            Dictionary with the label texts and whether an image is shown
        """
        seen = {}

        def inspect() -> None:
            dialog = app.activeModalWidget()
            labels = dialog.findChildren(QLabel)
            seen["texts"] = [label.text() for label in labels]
            seen["has_image"] = any(not label.pixmap().isNull() for label in labels)
            dialog.accept()

        QTimer.singleShot(0, inspect)
        window._show_sponsor()
        return seen

    def test_dialog_shows_qr_code(self, app, window, tmp_path):
        """Test that the Monero QR code image is shown when available."""
        import sponsor

        if not sponsor.QR_AVAILABLE:
            pytest.skip("qrcode or ImageMagick (Wand) not available")

        with patch("sponsor.tempfile.gettempdir", return_value=str(tmp_path)):
            seen = self._open(app, window)

        assert seen["has_image"] is True
        assert "PayPal:" in seen["texts"]

    def test_dialog_falls_back_to_address(self, app, window):
        """Test that the text address is shown when no QR code can be made."""
        import sponsor

        with patch("sponsor.QR_AVAILABLE", False):
            seen = self._open(app, window)

        assert seen["has_image"] is False
        assert sponsor.MONERO_ADDRESS in seen["texts"]
        assert TRANSLATIONS["en"]["qr_unavailable"] in seen["texts"]
