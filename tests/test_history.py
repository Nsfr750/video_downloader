"""Tests for the download history module."""

import json
import os
import sys
import threading
from unittest.mock import patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import history
from history import (
    STATUS_COMPLETED,
    STATUS_FAILED,
    DownloadHistory,
    HistoryEntry,
    get_history,
)


@pytest.fixture
def store(tmp_path):
    """Create a DownloadHistory stored in a temporary directory."""
    return DownloadHistory(str(tmp_path / "data" / "download_history.json"))


class TestHistoryEntry:
    """Test cases for HistoryEntry."""

    def test_defaults(self):
        """Test the default values of an entry."""
        entry = HistoryEntry(url="https://youtube.com/test")

        assert entry.status == STATUS_COMPLETED
        assert entry.completed is True
        assert entry.quality == "best"
        assert entry.format == "auto"
        assert entry.timestamp

    def test_failed_entry(self):
        """Test that a failed entry is not reported as completed."""
        entry = HistoryEntry(url="https://youtube.com/test", status=STATUS_FAILED)
        assert entry.completed is False

    def test_from_dict_ignores_unknown_keys(self):
        """Test that keys written by another version are ignored."""
        entry = HistoryEntry.from_dict(
            {"url": "https://youtube.com/test", "title": "Test", "unknown": 1}
        )
        assert entry.url == "https://youtube.com/test"
        assert entry.title == "Test"


class TestDownloadHistory:
    """Test cases for DownloadHistory."""

    def test_empty_history(self, store):
        """Test that a new history is empty and creates no file."""
        assert store.get_entries() == []
        assert len(store) == 0
        assert not os.path.exists(store.path)

    def test_add_creates_file(self, store):
        """Test that adding an entry writes the history file."""
        store.add(HistoryEntry(url="https://youtube.com/a", title="A"))

        assert os.path.isfile(store.path)
        with open(store.path, encoding="utf-8") as f:
            data = json.load(f)
        assert data[0]["url"] == "https://youtube.com/a"
        assert data[0]["title"] == "A"

    def test_entries_are_returned_newest_first(self, store):
        """Test the order of the entries."""
        for name in ("a", "b", "c"):
            store.add(HistoryEntry(url=f"https://youtube.com/{name}"))

        urls = [entry.url for entry in store.get_entries()]
        assert urls == [
            "https://youtube.com/c",
            "https://youtube.com/b",
            "https://youtube.com/a",
        ]

    def test_limit(self, store):
        """Test that only the newest entries are returned with a limit."""
        store.add_many([HistoryEntry(url=f"https://youtube.com/{i}") for i in range(5)])

        entries = store.get_entries(limit=2)
        assert [entry.url for entry in entries] == [
            "https://youtube.com/4",
            "https://youtube.com/3",
        ]

    def test_history_is_persistent(self, store):
        """Test that the entries are read back by another instance."""
        store.add(
            HistoryEntry(
                url="https://youtube.com/a",
                title="Título ü",
                status=STATUS_FAILED,
                quality="720p",
                format="mp4",
                file_path="downloads/a.mp4",
                playlist="List",
                error="boom",
            )
        )

        entry = DownloadHistory(store.path).get_entries()[0]
        assert entry.title == "Título ü"
        assert entry.status == STATUS_FAILED
        assert entry.quality == "720p"
        assert entry.format == "mp4"
        assert entry.file_path == "downloads/a.mp4"
        assert entry.playlist == "List"
        assert entry.error == "boom"

    def test_clear(self, store):
        """Test that clearing removes every entry."""
        store.add(HistoryEntry(url="https://youtube.com/a"))
        store.clear()

        assert store.get_entries() == []
        assert DownloadHistory(store.path).get_entries() == []

    def test_add_many_empty_does_nothing(self, store):
        """Test that adding no entries does not create the file."""
        store.add_many([])
        assert not os.path.exists(store.path)

    def test_max_entries(self, store):
        """Test that only the newest MAX_ENTRIES entries are kept."""
        with patch("history.MAX_ENTRIES", 3):
            store.add_many(
                [HistoryEntry(url=f"https://youtube.com/{i}") for i in range(5)]
            )

        assert [entry.url for entry in store.get_entries()] == [
            "https://youtube.com/4",
            "https://youtube.com/3",
            "https://youtube.com/2",
        ]

    @pytest.mark.parametrize("content", ["not json", '{"url": "x"}', ""])
    def test_corrupt_file_is_kept_as_backup(self, store, content):
        """Test that an unreadable history is set aside, not lost or fatal."""
        os.makedirs(os.path.dirname(store.path))
        with open(store.path, "w", encoding="utf-8") as f:
            f.write(content)

        assert store.get_entries() == []
        with open(store.path + ".bak", encoding="utf-8") as f:
            assert f.read() == content

        store.add(HistoryEntry(url="https://youtube.com/a"))
        assert len(store) == 1

    def test_invalid_items_are_skipped(self, store):
        """Test that malformed items do not hide the valid ones."""
        os.makedirs(os.path.dirname(store.path))
        with open(store.path, "w", encoding="utf-8") as f:
            json.dump(
                [{"title": "no url"}, "text", {"url": "https://youtube.com/a"}], f
            )

        assert [entry.url for entry in store.get_entries()] == ["https://youtube.com/a"]

    def test_concurrent_adds(self, store):
        """Test that entries added from several threads are all stored."""

        def add(index: int) -> None:
            store.add(HistoryEntry(url=f"https://youtube.com/{index}"))

        threads = [threading.Thread(target=add, args=(i,)) for i in range(20)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert len(store) == 20


class TestGlobalHistory:
    """Test cases for the global history instance."""

    def test_get_history_returns_same_instance(self):
        """Test that the global instance is shared."""
        assert get_history() is get_history()

    def test_get_history_default_path(self, monkeypatch):
        """Test the default location of the history file."""
        monkeypatch.setattr(history, "_history_instance", None)

        assert get_history().path == os.path.join("data", "download_history.json")


class TestHistoryMenu:
    """Test cases for the history shown in the CLI menu."""

    def _run(self, capsys, answers) -> str:
        """Run the history menu with the given answers.

        Args:
            capsys: pytest capture fixture
            answers: Values returned by input()

        Returns:
            Text printed by the menu
        """
        from menu import Menu

        with patch("builtins.input", side_effect=answers):
            Menu().history_menu()
        return capsys.readouterr().out

    def test_empty_history(self, english, capsys):
        """Test the message shown when nothing was downloaded."""
        assert "No downloads in history." in self._run(capsys, [""])

    def test_entries_are_listed(self, english, isolated_history, capsys):
        """Test that completed and failed downloads are listed."""
        isolated_history.add_many(
            [
                HistoryEntry(
                    url="https://youtube.com/a",
                    title="First video",
                    quality="720p",
                    format="mp4",
                    file_path="downloads/First video.mp4",
                ),
                HistoryEntry(
                    url="https://youtube.com/b", status=STATUS_FAILED, error="boom"
                ),
            ]
        )

        output = self._run(capsys, ["2"])

        assert "Completed - First video (720p, mp4)" in output
        assert "downloads/First video.mp4" in output
        assert "Failed - https://youtube.com/b" in output
        assert "Error: boom" in output
        assert output.index("https://youtube.com/b") < output.index("First video")
        assert len(isolated_history) == 2

    def test_clear_confirmed(self, english, isolated_history, capsys):
        """Test that the history is cleared after confirmation."""
        isolated_history.add(HistoryEntry(url="https://youtube.com/a"))

        output = self._run(capsys, ["1", "y"])

        assert "History cleared." in output
        assert len(isolated_history) == 0

    def test_clear_not_confirmed(self, english, isolated_history, capsys):
        """Test that the history is kept without confirmation."""
        isolated_history.add(HistoryEntry(url="https://youtube.com/a"))

        self._run(capsys, ["1", ""])

        assert len(isolated_history) == 1

    def test_main_menu_opens_history(self, english, capsys):
        """Test that the main menu option shows the history."""
        from menu import Menu

        with patch("builtins.input", side_effect=["7", "", "8"]):
            Menu().show_main_menu()

        assert "No downloads in history." in capsys.readouterr().out
