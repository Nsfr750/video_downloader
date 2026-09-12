"""Language package for Video Downloader application."""

from .language_manager import LanguageManager, get_language_manager, set_language, translate, _
from .translations import TRANSLATIONS

__all__ = [
    'LanguageManager',
    'get_language_manager',
    'set_language',
    'translate',
    '_',
    'TRANSLATIONS'
]
