"""Language management system for Video Downloader application.

This module provides functionality to manage multiple languages and translations.
"""

import os
from typing import Dict, Optional
from .translations import TRANSLATIONS


class LanguageManager:
    """Language manager class for handling multiple languages."""

    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'it': 'Italiano',
        'es': 'Español',
        'fr': 'Français',
        'de': 'Deutsch'
    }

    def __init__(self, default_language: str = 'en'):
        """Initialize the language manager.

        Args:
            default_language: Default language code (default: 'en')
        """
        self.current_language = default_language
        self.translations = TRANSLATIONS

    def set_language(self, language_code: str) -> bool:
        """Set the current language.

        Args:
            language_code: Language code (e.g., 'en', 'it', 'es')

        Returns:
            True if language was set successfully, False otherwise
        """
        if language_code in self.SUPPORTED_LANGUAGES:
            self.current_language = language_code
            return True
        return False

    def get_language(self) -> str:
        """Get the current language code.

        Returns:
            Current language code
        """
        return self.current_language

    def get_language_name(self) -> str:
        """Get the current language name.

        Returns:
            Current language name
        """
        return self.SUPPORTED_LANGUAGES.get(self.current_language, 'Unknown')

    def get_supported_languages(self) -> Dict[str, str]:
        """Get all supported languages.

        Returns:
            Dictionary of language codes and names
        """
        return self.SUPPORTED_LANGUAGES

    def translate(self, key: str, **kwargs) -> str:
        """Translate a key to the current language.

        Args:
            key: Translation key
            **kwargs: Variables for string formatting

        Returns:
            Translated string
        """
        # Get translation for current language
        translation = self.translations.get(self.current_language, {}).get(key)

        # Fallback to English if translation not found
        if translation is None:
            translation = self.translations.get('en', {}).get(key, key)

        # Format the translation with provided variables
        if kwargs:
            try:
                return translation.format(**kwargs)
            except (KeyError, ValueError):
                return translation

        return translation

    def get_all_translations(self) -> Dict[str, Dict[str, str]]:
        """Get all translations.

        Returns:
            Dictionary of all translations
        """
        return self.translations


# Global language manager instance
_language_manager_instance: Optional[LanguageManager] = None


def get_language_manager() -> LanguageManager:
    """Get the global language manager instance.

    Returns:
        Global language manager instance
    """
    global _language_manager_instance
    if _language_manager_instance is None:
        _language_manager_instance = LanguageManager()
    return _language_manager_instance


def set_language(language_code: str) -> bool:
    """Set the global language.

    Args:
        language_code: Language code (e.g., 'en', 'it', 'es')

    Returns:
        True if language was set successfully, False otherwise
    """
    manager = get_language_manager()
    return manager.set_language(language_code)


def translate(key: str, **kwargs) -> str:
    """Translate a key using the global language manager.

    Args:
        key: Translation key
        **kwargs: Variables for string formatting

    Returns:
        Translated string
    """
    manager = get_language_manager()
    return manager.translate(key, **kwargs)


def _(key: str, **kwargs) -> str:
    """Shorthand for translate function.

    Args:
        key: Translation key
        **kwargs: Variables for string formatting

    Returns:
        Translated string
    """
    return translate(key, **kwargs)
