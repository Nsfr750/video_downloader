"""Main application entry point for Video Downloader.

This module handles URL input and video download functionality using yt-dlp.
Supports both CLI and GUI modes.
"""

import os
import sys
import argparse
from typing import List, Optional
import yt_dlp
from logger import get_logger
from lang import get_language_manager, _
from version import __version__

COPYRIGHT = "© Copyright 2024-2026 Nsfr750 - All rights reserved."


class VideoDownloader:
    """Main video downloader class."""

    def __init__(self, download_dir: str = "downloads"):
        """Initialize the video downloader.

        Args:
            download_dir: Directory to save downloaded videos
        """
        self.download_dir = download_dir
        self.logger = get_logger()
        self.lang_manager = get_language_manager()

        # Create download directory if it doesn't exist
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            self.logger.info(f"Created download directory: {self.download_dir}")

    def get_urls_from_user(self) -> List[str]:
        """Get video URLs from user input.

        Returns:
            List of URLs to download
        """
        urls = []
        print(f"\n{_('enter_urls')}")

        while True:
            url = input("> ").strip()
            if not url:
                break
            urls.append(url)

        return urls

    def validate_url(self, url: str) -> bool:
        """Validate a URL.

        Args:
            url: URL to validate

        Returns:
            True if URL is valid, False otherwise
        """
        # Basic URL validation
        if not url.startswith(('http://', 'https://')):
            return False

        # Check for common video platforms
        supported_domains = [
            'youtube.com', 'youtu.be', 'vimeo.com', 'dailymotion.com',
            'twitch.tv', 'facebook.com', 'instagram.com', 'twitter.com',
            'tiktok.com', 'reddit.com', 'soundcloud.com'
        ]

        return any(domain in url.lower() for domain in supported_domains)

    def download_video(self, url: str) -> bool:
        """Download a video from the given URL.

        Args:
            url: URL of the video to download

        Returns:
            True if download was successful, False otherwise
        """
        try:
            self.logger.info(_('downloading').format(url=url))

            # Configure yt-dlp options
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
                'progress_hooks': [self._progress_hook],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.logger.info(_('download_complete').format(url=url))
            return True

        except Exception as e:
            self.logger.error(_('download_failed').format(url=url, error=str(e)))
            return False

    def _progress_hook(self, d: dict) -> None:
        """Progress hook for download progress.

        Args:
            d: Dictionary containing download progress information
        """
        if d['status'] == 'downloading':
            try:
                percent = d.get('_percent_str', '0%').replace('%', '')
                print(f"\r{_('download_progress').format(percent=float(percent))}", end='', flush=True)
            except (ValueError, AttributeError):
                pass
        elif d['status'] == 'finished':
            print()  # New line after progress

    def download_videos(self, urls: List[str]) -> None:
        """Download multiple videos.

        Args:
            urls: List of URLs to download
        """
        if not urls:
            print(_('no_urls'))
            return

        print(f"\nDownloading {len(urls)} videos...\n")

        successful = 0
        failed = 0

        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] ", end='')

            if not self.validate_url(url):
                print(_('invalid_url').format(url=url))
                self.logger.warning(_('invalid_url').format(url=url))
                failed += 1
                continue

            if self.download_video(url):
                successful += 1
            else:
                failed += 1

        print(f"\n\n{'='*50}")
        print(f"Download Summary:")
        print(f"  Successful: {successful}")
        print(f"  Failed: {failed}")
        print(f"  Total: {len(urls)}")
        print(f"{'='*50}\n")


def main() -> None:
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description=_('app_title'))
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Run in CLI mode (default is GUI mode)'
    )
    parser.add_argument(
        '--gui',
        action='store_true',
        help='Run in GUI mode (default)'
    )
    args = parser.parse_args()

    # Determine mode: --gui for GUI, --cli for CLI, default to GUI
    if args.gui:
        use_gui = True
    elif args.cli:
        use_gui = False
    else:
        use_gui = True  # Default to GUI mode

    if use_gui:
        try:
            from ui.main_window import run_gui
            run_gui()
        except ImportError:
            print("PySide6 not installed. Falling back to CLI mode.")
            print("Install PySide6 with: pip install PySide6")
            _run_cli()
    else:
        _run_cli()


def _run_cli() -> None:
    """Run the application in CLI mode."""
    print(f"\n{_('app_title')}")
    print(f"Version: {__version__}")
    print(f"{COPYRIGHT}\n")

    # Show main menu
    from menu import show_main_menu
    show_main_menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n{_('error')}: {e}")
        sys.exit(1)
