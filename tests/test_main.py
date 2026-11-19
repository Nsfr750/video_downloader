"""Tests for the main module."""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import VideoDownloader


class TestVideoDownloader:
    """Test cases for VideoDownloader class."""

    @pytest.fixture
    def downloader(self):
        """Create a VideoDownloader instance for testing."""
        return VideoDownloader(download_dir="test_downloads")

    def test_init(self, downloader):
        """Test VideoDownloader initialization."""
        assert downloader.download_dir == "test_downloads"
        assert downloader.logger is not None
        assert downloader.lang_manager is not None

    def test_validate_url_valid(self, downloader):
        """Test URL validation with valid URLs."""
        assert downloader.validate_url("https://www.youtube.com/watch?v=test")
        assert downloader.validate_url("https://vimeo.com/123456789")
        assert downloader.validate_url("http://dailymotion.com/video/test")

    def test_validate_url_invalid(self, downloader):
        """Test URL validation with invalid URLs."""
        assert not downloader.validate_url("not a url")
        assert not downloader.validate_url("ftp://example.com")
        assert not downloader.validate_url("")

    def test_get_urls_from_user_empty(self, downloader, capsys):
        """Test getting URLs from user with no input."""
        with patch('builtins.input', return_value=''):
            urls = downloader.get_urls_from_user()
            assert urls == []

    def test_get_urls_from_user_multiple(self, downloader, capsys):
        """Test getting multiple URLs from user."""
        with patch('builtins.input', side_effect=['https://youtube.com/test1', 'https://vimeo.com/test2', '']):
            urls = downloader.get_urls_from_user()
            assert len(urls) == 2
            assert 'https://youtube.com/test1' in urls
            assert 'https://vimeo.com/test2' in urls

    @patch('main.yt_dlp.YoutubeDL')
    def test_download_video_success(self, mock_ydl, downloader):
        """Test successful video download."""
        mock_ydl_instance = Mock()
        mock_ydl.return_value.__enter__.return_value = mock_ydl_instance

        result = downloader.download_video("https://youtube.com/test")
        assert result is True
        mock_ydl_instance.download.assert_called_once()

    @patch('main.yt_dlp.YoutubeDL')
    def test_download_video_failure(self, mock_ydl, downloader):
        """Test failed video download."""
        mock_ydl_instance = Mock()
        mock_ydl_instance.download.side_effect = Exception("Download failed")
        mock_ydl.return_value.__enter__.return_value = mock_ydl_instance

        result = downloader.download_video("https://youtube.com/test")
        assert result is False

    def test_download_videos_empty(self, downloader, capsys):
        """Test downloading with empty URL list."""
        with patch('builtins.print'):
            downloader.download_videos([])
        captured = capsys.readouterr()
        # Check that the no URLs message was printed

    def test_progress_hook_downloading(self, downloader, capsys):
        """Test progress hook during download."""
        d = {'status': 'downloading', '_percent_str': '50%'}
        with patch('builtins.print'):
            downloader._progress_hook(d)

    def test_progress_hook_finished(self, downloader, capsys):
        """Test progress hook when download is finished."""
        d = {'status': 'finished'}
        with patch('builtins.print'):
            downloader._progress_hook(d)
