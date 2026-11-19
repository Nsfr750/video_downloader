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
1. Installation (Python 3.13 or higher):
   py -3.13 -m pip install -r requirements.txt

2. Running the application:
   py -3.13 main.py          (GUI mode, default)
   py -3.13 main.py --cli    (CLI mode)

3. Downloading videos:
   - Select 'Download Videos' from the main menu
   - Choose the quality: best, worst, 1080p, 720p, 480p, 360p or audio only
   - Choose the output format: auto (keep original), mp4, webm, mkv, avi,
     mp3, m4a or wav
   - Choose whether playlists must be downloaded entirely
   - Enter one or more video URLs (one per line)
   - Press Enter on an empty line to start downloading
   - Videos will be saved to the 'downloads' folder

4. Playlists:
   - With the playlist option enabled, every video of a playlist URL is
     downloaded into a folder named after the playlist, with numbered files
   - A video that cannot be downloaded does not stop the rest of the playlist
   - With the option disabled, a playlist URL downloads a single video

5. Download history:
   - Every downloaded or failed video is recorded in
     'data/download_history.json'
   - View the history from the main menu (CLI) or the history tab (GUI)
   - The history can be cleared from the same place

6. Supported platforms:
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

7. Language support:
   - English
   - Italian
   - Spanish
   - French
   - German

8. Logging:
   - All activities are logged to the 'logs' folder
   - View logs from the main menu
   - Logs are organized by date

9. Updates:
   - Check for updates from the main menu
   - Updates are checked against the latest release on GitHub

10. Sponsor:
   - Support the project with PayPal or Monero
   - The GUI shows a QR code for the Monero address
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
   - Try updating yt-dlp: py -3.13 -m pip install --upgrade yt-dlp
   - The reason of each failure is shown in the download history

2. YouTube: "Requested format is not available":
   - yt-dlp needs a JavaScript runtime (Deno) to read all YouTube formats
   - Install Deno, or try another quality

3. Only one video of a playlist is downloaded:
   - Enable the playlist option before starting the download

4. Slow download speed:
   - Download speed depends on your internet connection
   - Some platforms limit download speeds
   - Try downloading during off-peak hours

5. Logs not appearing:
   - Check that the 'logs' folder exists
   - Ensure you have write permissions
   - Check the log level in logger.py

6. Download history is empty after an error:
   - An unreadable history file is renamed to 'download_history.json.bak'
     and a new history is started

7. Monero QR code not shown:
   - The QR code needs the qrcode package and ImageMagick (used by Wand)
   - Without them the Monero address is shown as text

8. Permission errors:
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
