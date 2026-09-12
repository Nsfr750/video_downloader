"""Tests for the language system."""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lang.language_manager import LanguageManager, get_language_manager, set_language, translate, _


class TestLanguageManager:
    """Test cases for LanguageManager class."""

    @pytest.fixture
    def lang_manager(self):
        """Create a LanguageManager instance for testing."""
        return LanguageManager()

    def test_init_default_language(self, lang_manager):
        """Test initialization with default language."""
        assert lang_manager.current_language == 'en'

    def test_init_custom_language(self):
        """Test initialization with custom language."""
        manager = LanguageManager(default_language='it')
        assert manager.current_language == 'it'

    def test_set_language_valid(self, lang_manager):
        """Test setting a valid language."""
        assert lang_manager.set_language('it') is True
        assert lang_manager.current_language == 'it'

    def test_set_language_invalid(self, lang_manager):
        """Test setting an invalid language."""
        assert lang_manager.set_language('invalid') is False
        assert lang_manager.current_language == 'en'

    def test_get_language(self, lang_manager):
        """Test getting current language code."""
        lang_manager.set_language('es')
        assert lang_manager.get_language() == 'es'

    def test_get_language_name(self, lang_manager):
        """Test getting current language name."""
        lang_manager.set_language('fr')
        assert lang_manager.get_language_name() == 'Français'

    def test_get_supported_languages(self, lang_manager):
        """Test getting supported languages."""
        languages = lang_manager.get_supported_languages()
        assert 'en' in languages
        assert 'it' in languages
        assert 'es' in languages
        assert 'fr' in languages
        assert 'de' in languages

    def test_translate_english(self, lang_manager):
        """Test translation in English."""
        lang_manager.set_language('en')
        result = lang_manager.translate('app_name')
        assert result == 'Video Downloader'

    def test_translate_italian(self, lang_manager):
        """Test translation in Italian."""
        lang_manager.set_language('it')
        result = lang_manager.translate('app_name')
        assert result == 'Video Downloader'

    def test_translate_with_variables(self, lang_manager):
        """Test translation with variables."""
        lang_manager.set_language('en')
        result = lang_manager.translate('downloading', url='test_url')
        assert 'test_url' in result

    def test_translate_fallback_to_english(self, lang_manager):
        """Test fallback to English for missing translations."""
        lang_manager.set_language('en')
        result = lang_manager.translate('nonexistent_key')
        assert result == 'nonexistent_key'


class TestGlobalLanguageFunctions:
    """Test cases for global language functions."""

    def test_get_language_manager_singleton(self):
        """Test that get_language_manager returns the same instance."""
        manager1 = get_language_manager()
        manager2 = get_language_manager()
        assert manager1 is manager2

    def test_set_language_global(self):
        """Test setting language globally."""
        assert set_language('de') is True
        manager = get_language_manager()
        assert manager.get_language() == 'de'

    def test_translate_global(self):
        """Test global translate function."""
        set_language('en')
        result = translate('app_name')
        assert result == 'Video Downloader'

    def test_shorthand_translate(self):
        """Test shorthand translate function."""
        set_language('en')
        result = _('app_name')
        assert result == 'Video Downloader'
