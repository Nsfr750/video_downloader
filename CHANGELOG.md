# Changelog

All notable changes to Video Downloader will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-11-18

### Added
- QR code for Monero donations in sponsor dialog
- Python 3.13 support with pyproject.toml configuration
- .python-version file for pyenv
- Quality selection options for video downloads (best, worst, 1080p, 720p, 480p, 360p, audio)
- Format conversion options (auto, mp4, webm, mkv, avi, mp3, m4a, wav)
- Quality selection dropdown in GUI
- Format selection dropdown in GUI
- Quality selection menu in CLI
- Format selection menu in CLI
- Playlist support: optional download of entire playlists, saved in a folder named after the playlist with numbered files
- Download history: every downloaded or failed video is recorded in `data/download_history.json`
- "Download History" menu in CLI and "Download History" tab in GUI, with clear function
- Shared download core (`download_core.py`) used by both CLI and GUI
- Tests for quality/format selection, update check, sponsor QR code, playlists and download history

### Changed
- Improved update check logic to properly handle version comparison
- Updated sponsor dialog to display QR code instead of text address
- Better error handling for GitHub API 404 errors
- Updated copyright from Nsfr750 to Tuxxle
- Fixed GUI translations for all hardcoded text
- A playlist URL downloads a single video unless the playlist option is enabled
- Download summary counts videos instead of URLs
- CLI main menu: "Download History" is option 7, "Exit" is now option 8

### Fixed
- Update system now correctly shows "latest version" message when no update is available
- Fixed syntax error in main_window.py
- All GUI text now properly translates when language is changed

## [1.0.0] - 2026-09-12

### Added
- Initial release
- Video download functionality using yt-dlp
- Multi-URL support
- Language system with support for English, Italian, Spanish, French, and German
- Logging system
- Menu interface
- Help system
- About and sponsor pages
- Update system
- Graphical User Interface (GUI) with PySide6
- Command Line Interface (CLI) mode with --cli flag
- Download progress indicators
- Log viewer in GUI
- Language switching in GUI
- GPLv3 LICENSE file
- SECURITY.md for security reporting
- Clean pycache script
