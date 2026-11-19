"""Download history for Video Downloader application.

This module stores the list of downloaded (and failed) videos in a JSON file
so that it can be shown again in the CLI and in the GUI.
"""

import json
import os
import threading
from dataclasses import asdict, dataclass, field, fields
from datetime import datetime
from typing import Any, Dict, List, Optional

from logger import get_logger

HISTORY_DIR = "data"
HISTORY_FILE = "download_history.json"
MAX_ENTRIES = 1000

STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"


def _now() -> str:
    """Return the current local time as an ISO 8601 string.

    Returns:
        Timestamp with seconds precision
    """
    return datetime.now().isoformat(timespec="seconds")


@dataclass
class HistoryEntry:
    """A single download recorded in the history."""

    url: str
    title: str = ""
    status: str = STATUS_COMPLETED
    quality: str = "best"
    format: str = "auto"
    file_path: str = ""
    playlist: str = ""
    error: str = ""
    timestamp: str = field(default_factory=_now)

    @property
    def completed(self) -> bool:
        """Tell whether the download was successful.

        Returns:
            True if the download completed, False if it failed
        """
        return self.status == STATUS_COMPLETED

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HistoryEntry":
        """Create an entry from a dictionary, ignoring unknown keys.

        Args:
            data: Dictionary read from the history file

        Returns:
            History entry
        """
        known = {f.name for f in fields(cls)}
        return cls(**{key: value for key, value in data.items() if key in known})


class DownloadHistory:
    """Persistent download history stored in a JSON file."""

    def __init__(self, path: Optional[str] = None):
        """Initialize the download history.

        Args:
            path: Path of the history file (default: data/download_history.json)
        """
        self.path = path or os.path.join(HISTORY_DIR, HISTORY_FILE)
        self.logger = get_logger()
        self._lock = threading.Lock()

    def _load(self) -> List[HistoryEntry]:
        """Read the entries from the history file, oldest first.

        An unreadable file is kept aside as ``<name>.bak`` and treated as empty.

        Returns:
            List of history entries
        """
        if not os.path.exists(self.path):
            return []

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("history file does not contain a list")
        except (OSError, ValueError) as e:
            self.logger.warning(f"Could not read download history: {e}")
            try:
                os.replace(self.path, self.path + ".bak")
            except OSError:
                pass
            return []

        entries = []
        for item in data:
            try:
                entries.append(HistoryEntry.from_dict(item))
            except (TypeError, AttributeError):
                continue
        return entries

    def _save(self, entries: List[HistoryEntry]) -> None:
        """Write the entries to the history file.

        Args:
            entries: Entries to store, oldest first
        """
        directory = os.path.dirname(self.path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        temp_path = self.path + ".tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(
                [asdict(entry) for entry in entries], f, ensure_ascii=False, indent=2
            )
        os.replace(temp_path, self.path)

    def add(self, entry: HistoryEntry) -> None:
        """Add an entry to the history.

        Args:
            entry: Entry to add
        """
        self.add_many([entry])

    def add_many(self, entries: List[HistoryEntry]) -> None:
        """Add several entries to the history, keeping the newest MAX_ENTRIES.

        Args:
            entries: Entries to add, oldest first
        """
        if not entries:
            return
        with self._lock:
            stored = self._load()
            stored.extend(entries)
            self._save(stored[-MAX_ENTRIES:])

    def get_entries(self, limit: Optional[int] = None) -> List[HistoryEntry]:
        """Get the history entries, newest first.

        Args:
            limit: Maximum number of entries to return (default: all)

        Returns:
            List of history entries
        """
        with self._lock:
            entries = self._load()
        entries.reverse()
        return entries if limit is None else entries[:limit]

    def clear(self) -> None:
        """Remove all the entries from the history."""
        with self._lock:
            self._save([])

    def __len__(self) -> int:
        """Get the number of entries in the history.

        Returns:
            Number of entries
        """
        return len(self.get_entries())


# Global history instance
_history_instance: Optional[DownloadHistory] = None


def get_history() -> DownloadHistory:
    """Get the global download history instance.

    Returns:
        Global download history instance
    """
    global _history_instance
    if _history_instance is None:
        _history_instance = DownloadHistory()
    return _history_instance
