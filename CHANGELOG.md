# Changelog

All notable changes to Video Downloader will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-11-17

### Added
- QR code for Monero donations in sponsor dialog
- Python 3.13 support with pyproject.toml configuration
- .python-version file for pyenv

### Changed
- Improved update check logic to properly handle version comparison
- Updated sponsor dialog to display QR code instead of text address
- Better error handling for GitHub API 404 errors

### Fixed
- Update system now correctly shows "latest version" message when no update is available

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
