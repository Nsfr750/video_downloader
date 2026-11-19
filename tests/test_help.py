"""Tests for the help module and the help shown in the CLI and the GUI."""

import os
import re
import sys
from unittest.mock import patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import help as help_module
from lang import get_language_manager
from lang.translations import TRANSLATIONS

OTHER_LANGUAGES = sorted(set(TRANSLATIONS) - {"en"})
HELP_KEYS = ["help_content", "usage_content", "troubleshooting_content"]
TITLE_KEYS = ["usage_title", "troubleshooting_title"]


@pytest.fixture
def language():
    """Return a function selecting a language, restored after the test."""
    manager = get_language_manager()
    previous = manager.get_language()
    yield manager.set_language
    manager.set_language(previous)


def _sections(text: str) -> list:
    """Return the section numbers of a help text."""
    return re.findall(r"^(\d+)\. ", text, re.M)


class TestHelpTranslations:
    """Test cases for the translated help texts."""

    @pytest.mark.parametrize("code", OTHER_LANGUAGES)
    @pytest.mark.parametrize("key", HELP_KEYS + TITLE_KEYS)
    def test_texts_are_translated(self, code, key):
        """Test that no help text is left in English."""
        assert TRANSLATIONS[code][key] != TRANSLATIONS["en"][key]

    @pytest.mark.parametrize("code", sorted(TRANSLATIONS))
    @pytest.mark.parametrize("key", HELP_KEYS)
    def test_same_sections_in_every_language(self, code, key):
        """Test that every language has the same numbered sections."""
        assert _sections(TRANSLATIONS[code][key]) == _sections(TRANSLATIONS["en"][key])

    @pytest.mark.parametrize("code", sorted(TRANSLATIONS))
    def test_commands_and_paths_are_not_translated(self, code):
        """Test that commands, file names and contacts are kept verbatim."""
        usage = TRANSLATIONS[code]["usage_content"]
        trouble = TRANSLATIONS[code]["troubleshooting_content"]

        assert "py -3.13 -m pip install -r requirements.txt" in usage
        assert "py -3.13 main.py --cli" in usage
        assert "data/download_history.json" in usage
        assert "py -3.13 -m pip install --upgrade yt-dlp" in trouble
        assert "download_history.json.bak" in trouble
        assert "nsfr750@yandex.com" in trouble
        assert "https://www.tuxxle.org" in trouble

    @pytest.mark.parametrize("code", sorted(TRANSLATIONS))
    def test_usage_guide_names_the_download_menu(self, code):
        """Test that the guide uses the menu label of the same language."""
        strings = TRANSLATIONS[code]
        assert f"'{strings['menu_download']}'" in strings["usage_content"]


class TestHelpModule:
    """Test cases for the functions of help.py."""

    @pytest.mark.parametrize("code", sorted(TRANSLATIONS))
    def test_show_usage_guide(self, language, capsys, code):
        """Test that the usage guide is printed in the current language."""
        language(code)
        help_module.show_usage_guide()

        output = capsys.readouterr().out
        assert TRANSLATIONS[code]["usage_title"] in output
        assert TRANSLATIONS[code]["usage_content"] in output

    @pytest.mark.parametrize("code", sorted(TRANSLATIONS))
    def test_show_troubleshooting(self, language, capsys, code):
        """Test that troubleshooting is printed in the current language."""
        language(code)
        help_module.show_troubleshooting()

        output = capsys.readouterr().out
        assert TRANSLATIONS[code]["troubleshooting_title"] in output
        assert TRANSLATIONS[code]["troubleshooting_content"] in output


class TestHelpMenu:
    """Test cases for the help shown in the CLI menu."""

    def _run(self, capsys, answers) -> str:
        """Run the help menu with the given answers.

        Args:
            capsys: pytest capture fixture
            answers: Values returned by input()

        Returns:
            Text printed by the menu
        """
        from menu import Menu

        with patch("builtins.input", side_effect=answers):
            Menu().show_help()
        return capsys.readouterr().out

    def test_help_only(self, language, capsys):
        """Test that going back shows only the main help."""
        language("en")
        output = self._run(capsys, ["3"])

        assert TRANSLATIONS["en"]["help_content"] in output
        assert "1. Usage Guide" in output
        assert "2. Troubleshooting" in output
        assert TRANSLATIONS["en"]["usage_content"] not in output

    def test_usage_guide_and_troubleshooting(self, language, capsys):
        """Test that both extra pages can be opened from the help menu."""
        language("it")
        output = self._run(capsys, ["1", "2", ""])

        assert TRANSLATIONS["it"]["usage_content"] in output
        assert TRANSLATIONS["it"]["troubleshooting_content"] in output


class TestHelpDialog:
    """Test cases for the help dialog of the GUI."""

    @pytest.mark.parametrize("code", ["en", "it", "de"])
    def test_dialog_tabs(self, language, code):
        """Test that the dialog shows the three help pages, translated."""
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        pytest.importorskip("PySide6")
        from PySide6.QtCore import QTimer
        from PySide6.QtWidgets import QApplication, QTabWidget, QTextEdit

        from ui.main_window import MainWindow

        app = QApplication.instance() or QApplication([])
        language(code)
        window = MainWindow()
        seen = {}

        def inspect() -> None:
            dialog = app.activeModalWidget()
            tabs = dialog.findChild(QTabWidget)
            seen["titles"] = [tabs.tabText(i) for i in range(tabs.count())]
            seen["texts"] = [
                tabs.widget(i).toPlainText() for i in range(tabs.count())
            ]
            seen["read_only"] = all(
                page.isReadOnly() for page in dialog.findChildren(QTextEdit)
            )
            dialog.accept()

        QTimer.singleShot(0, inspect)
        window._show_help()
        window.close()

        strings = TRANSLATIONS[code]
        assert seen["titles"] == [
            strings["help_title"],
            strings["usage_title"],
            strings["troubleshooting_title"],
        ]
        assert seen["texts"] == [
            strings["help_content"].strip(),
            strings["usage_content"].strip(),
            strings["troubleshooting_content"].strip(),
        ]
        assert seen["read_only"] is True
