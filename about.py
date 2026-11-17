"""About information for Video Downloader application.

This module provides information about the application, author, and credits.
"""

from lang import _
from version import __version__

COPYRIGHT = "© Copyright 2024-2026 Tuxxle - All rights reserved."


def show_about() -> None:
    """Display about information."""
    print(f"\n{'='*50}")
    print(f"{_('about_title')}")
    print(f"{'='*50}")
    print(_('about_content').format(__version__))
    print(f"{'='*50}\n")


def show_credits() -> None:
    """Display credits and acknowledgments."""
    print(f"\n{'='*50}")
    print("Credits")
    print(f"{'='*50}")
    print("""
Development:
- Nsfr750 (Lead Developer)

Libraries Used:
- yt-dlp: Video downloading library
- Wand: Image processing library

Special Thanks:
- yt-dlp community for the excellent library
- All contributors and testers

Organization:
- Tuxxle

License:
- GPLv3 (GNU General Public License v3.0)
    """)
    print(f"{'='*50}\n")


def show_contact_info() -> None:
    """Display contact information."""
    print(f"\n{'='*50}")
    print("Contact Information")
    print(f"{'='*50}")
    print("""
Author: Nsfr750
Email: nsfr750@yandex.com
Website: https://www.tuxxle.org
GitHub: https://github.com/Nsfr750
Security Report: info@tuxxle.org

Organization: Tuxxle
    """)
    print(f"{'='*50}\n")


if __name__ == "__main__":
    show_about()
    show_credits()
    show_contact_info()
