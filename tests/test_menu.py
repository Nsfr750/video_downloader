"""Tests for the menu module."""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from menu import Menu


class TestMenu:
    """Test cases for Menu class."""

    @pytest.fixture
    def menu(self):
        """Create a Menu instance for testing."""
        return Menu()

    def test_init(self, menu):
        """Test menu initialization."""
        assert menu.logger is not None
        assert menu.lang_manager is not None

    @patch('builtins.input', side_effect=['8'])  # Exit option
    def test_show_main_menu_exit(self, mock_input, menu):
        """Test main menu with exit option."""
        menu.show_main_menu()
        mock_input.assert_called()

    @patch('builtins.input', side_effect=['1', '', '', '', '', '8'])  # Download, default quality, default format, no playlist, empty URL, exit
    def test_download_menu_empty_urls(self, mock_input, menu):
        """Test download menu with empty URLs."""
        menu.show_main_menu()

    @patch('builtins.input', side_effect=['3', '1', '8'])  # Language, English, exit
    def test_language_menu_select_english(self, mock_input, menu):
        """Test language menu selecting English."""
        menu.show_main_menu()

    @patch('builtins.input', side_effect=['4', '', '8'])  # Help, press enter, exit
    def test_show_help(self, mock_input, menu):
        """Test showing help."""
        menu.show_main_menu()

    @patch('builtins.input', side_effect=['5', '', '8'])  # About, press enter, exit
    def test_show_about(self, mock_input, menu):
        """Test showing about."""
        menu.show_main_menu()

    @patch('builtins.input', side_effect=['6', '', '8'])  # Update, press enter, exit
    def test_check_updates(self, mock_input, menu):
        """Test checking for updates."""
        menu.show_main_menu()

    @patch('builtins.input', side_effect=['2', '4', '8'])  # View logs, back, exit
    def test_view_logs_menu(self, mock_input, menu):
        """Test viewing logs menu."""
        menu.show_main_menu()
