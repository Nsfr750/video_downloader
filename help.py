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
    print("Usage Guide")
    print(f"{'='*50}")
    print("""
1. Installation:
   pip install -r requirements.txt

2. Running the application:
   python main.py

3. Downloading videos:
   - Select 'Download Videos' from the main menu
   - Enter one or more video URLs (one per line)
   - Press Enter on an empty line to start downloading
   - Videos will be saved to the 'downloads' folder

4. Supported platforms:
   - YouTube
   - Vimeo
   - Dailymotion
   - Twitch
   - Facebook
   - Instagram
   - Twitter/X
   - TikTok
   - Reddit
   - SoundCloud
   - And many more...

5. Language support:
   - English
   - Italian
   - Spanish
   - French
   - German

6. Logging:
   - All activities are logged to the 'logs' folder
   - View logs from the main menu
   - Logs are organized by date

7. Updates:
   - Check for updates from the main menu
   - Updates are checked against the latest version
    """)
    print(f"{'='*50}\n")


def show_troubleshooting() -> None:
    """Display troubleshooting information."""
    print(f"\n{'='*50}")
    print("Troubleshooting")
    print(f"{'='*50}")
    print("""
Common Issues and Solutions:

1. Download fails:
   - Check your internet connection
   - Verify the URL is correct
   - Some videos may be region-locked or private
   - Try updating yt-dlp: pip install --upgrade yt-dlp

2. Slow download speed:
   - Download speed depends on your internet connection
   - Some platforms limit download speeds
   - Try downloading during off-peak hours

3. Language not changing:
   - Restart the application after changing language
   - Check that the language code is correct

4. Logs not appearing:
   - Check that the 'logs' folder exists
   - Ensure you have write permissions
   - Check the log level in logger.py

5. Permission errors:
   - Ensure you have write permissions for the download directory
   - Try running as administrator (Windows) or with sudo (Linux/Mac)

For more help:
- Email: nsfr750@yandex.com
- Website: https://www.tuxxle.org
- GitHub: https://github.com/Nsfr750
    """)
    print(f"{'='*50}\n")


if __name__ == "__main__":
    show_help()
    show_usage_guide()
    show_troubleshooting()
