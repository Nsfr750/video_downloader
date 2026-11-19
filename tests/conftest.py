"""Shared fixtures for the Video Downloader tests."""

import os
import sys

import pytest

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import history


@pytest.fixture(autouse=True)
def isolated_history(tmp_path, monkeypatch):
    """Use a temporary download history so tests never touch the real one."""
    instance = history.DownloadHistory(str(tmp_path / "history" / "history.json"))
    monkeypatch.setattr(history, "_history_instance", instance)
    return instance


@pytest.fixture
def english():
    """Force the English language for the duration of a test."""
    from lang import get_language_manager

    manager = get_language_manager()
    previous = manager.get_language()
    manager.set_language("en")
    yield manager
    manager.set_language(previous)
