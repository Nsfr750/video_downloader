"""Help system for Video Downloader application.

This module provides help documentation and information.
"""

from lang import _


def show_help() -> None:
    """Display help information."""
    print(f"\n{'='*50}")
    print(f"{_('help_title')}")
    print(f"{'='*50}")
    print(_('help_content'))
    print(f"{'='*50}\n")


def show_usage_guide() -> None:
    """Display detailed usage guide."""
    print(f"\n{'='*50}")
    print(f"{_('usage_title')}")
    print(f"{'='*50}")
    print(_('usage_content'))
    print(f"{'='*50}\n")


def show_troubleshooting() -> None:
    """Display troubleshooting information."""
    print(f"\n{'='*50}")
    print(f"{_('troubleshooting_title')}")
    print(f"{'='*50}")
    print(_('troubleshooting_content'))
    print(f"{'='*50}\n")


if __name__ == "__main__":
    show_help()
    show_usage_guide()
    show_troubleshooting()
