"""Tests for the update module."""

import json
import os
import sys
import urllib.error
from unittest.mock import MagicMock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from update import GITHUB_API_URL, UpdateManager
from version import __version__


def _response(payload) -> MagicMock:
    """Build a fake urlopen response returning the given payload.

    Args:
        payload: Object to serialize as JSON, or raw bytes

    Returns:
        Mock usable as the context manager returned by urlopen
    """
    body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
    response = MagicMock()
    response.__enter__.return_value.read.return_value = body
    return response


class TestUpdateManager:
    """Test cases for UpdateManager class."""

    @pytest.fixture
    def manager(self):
        """Create an UpdateManager instance for testing."""
        return UpdateManager()

    @patch("update.urllib.request.urlopen")
    def test_check_for_updates_newer_version(self, mock_urlopen, manager):
        """Test that a newer release is returned without the 'v' prefix."""
        mock_urlopen.return_value = _response({"tag_name": "v99.0.0"})

        assert manager.check_for_updates() == "99.0.0"
        assert mock_urlopen.call_args.args[0] == GITHUB_API_URL

    @patch("update.urllib.request.urlopen")
    def test_check_for_updates_same_version(self, mock_urlopen, manager):
        """Test that the current version is returned, not treated as an error."""
        mock_urlopen.return_value = _response({"tag_name": f"v{__version__}"})

        latest = manager.check_for_updates()
        assert latest == __version__
        assert manager._compare_versions(latest, __version__) == 0

    @patch("update.urllib.request.urlopen")
    def test_check_for_updates_tag_without_prefix(self, mock_urlopen, manager):
        """Test that a tag without the 'v' prefix is accepted."""
        mock_urlopen.return_value = _response({"tag_name": "2.3.4"})

        assert manager.check_for_updates() == "2.3.4"

    @patch("update.urllib.request.urlopen")
    def test_check_for_updates_missing_tag(self, mock_urlopen, manager):
        """Test that a release without a tag gives no version."""
        mock_urlopen.return_value = _response({})

        assert not manager.check_for_updates()

    @patch("update.urllib.request.urlopen")
    def test_check_for_updates_not_found(self, mock_urlopen, manager):
        """Test that a 404 (no releases or private repository) returns None."""
        mock_urlopen.side_effect = urllib.error.HTTPError(
            GITHUB_API_URL, 404, "Not Found", None, None
        )

        assert manager.check_for_updates() is None

    @patch("update.urllib.request.urlopen")
    def test_check_for_updates_http_error(self, mock_urlopen, manager):
        """Test that another HTTP error returns None."""
        mock_urlopen.side_effect = urllib.error.HTTPError(
            GITHUB_API_URL, 500, "Server Error", None, None
        )

        assert manager.check_for_updates() is None

    @patch("update.urllib.request.urlopen")
    def test_check_for_updates_network_error(self, mock_urlopen, manager):
        """Test that a network error returns None."""
        mock_urlopen.side_effect = urllib.error.URLError("no connection")

        assert manager.check_for_updates() is None

    @patch("update.urllib.request.urlopen")
    def test_check_for_updates_invalid_json(self, mock_urlopen, manager):
        """Test that an unreadable answer returns None."""
        mock_urlopen.return_value = _response(b"not json")

        assert manager.check_for_updates() is None

    @pytest.mark.parametrize(
        "version1, version2, expected",
        [
            ("1.1.0", "1.0.0", 1),
            ("1.0.0", "1.1.0", -1),
            ("1.1.0", "1.1.0", 0),
            ("2.0.0", "1.9.9", 1),
            ("1.10.0", "1.9.0", 1),
            ("1.1", "1.1.0", 0),
            ("1.1.0.1", "1.1.0", 1),
        ],
    )
    def test_compare_versions(self, manager, version1, version2, expected):
        """Test version comparison."""
        assert manager._compare_versions(version1, version2) == expected

    @patch("update.urllib.request.urlopen")
    def test_get_release_notes(self, mock_urlopen, manager):
        """Test that release notes are read from the release body."""
        mock_urlopen.return_value = _response({"body": "Fixed bugs"})

        assert manager.get_release_notes() == "Fixed bugs"

    @patch("update.urllib.request.urlopen")
    def test_get_release_notes_error(self, mock_urlopen, manager):
        """Test that release notes are None when the request fails."""
        mock_urlopen.side_effect = urllib.error.URLError("no connection")

        assert manager.get_release_notes() is None


class TestUpdateMenu:
    """Test cases for the update check shown in the CLI menu."""

    @pytest.fixture
    def english(self):
        """Force the English language for the duration of a test."""
        from lang import get_language_manager

        manager = get_language_manager()
        previous = manager.get_language()
        manager.set_language("en")
        yield manager
        manager.set_language(previous)

    def _run(self, capsys, latest) -> str:
        """Run the menu update check with a mocked latest version.

        Args:
            capsys: pytest capture fixture
            latest: Value returned by UpdateManager.check_for_updates

        Returns:
            Text printed by the menu
        """
        from menu import Menu

        with (
            patch("update.UpdateManager.check_for_updates", return_value=latest),
            patch("builtins.input", return_value=""),
        ):
            Menu().check_updates()
        return capsys.readouterr().out

    def test_menu_reports_latest_version(self, english, capsys):
        """Test that an up-to-date app is not reported as an error."""
        output = self._run(capsys, __version__)

        assert "You are using the latest version" in output
        assert "Error checking for updates" not in output

    def test_menu_reports_available_update(self, english, capsys):
        """Test that a newer release is announced."""
        assert "Update available: 99.0.0" in self._run(capsys, "99.0.0")

    def test_menu_reports_error(self, english, capsys):
        """Test that a failed check is reported as an error."""
        assert "Error checking for updates" in self._run(capsys, None)
