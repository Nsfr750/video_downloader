# Video Downloader Project Structure

## Overview
Video Downloader is a Python application for downloading videos from the internet using yt-dlp.

## Directory Structure

```
video_downloader/
├── main.py                 # Main application entry point
├── version.py              # Version information (Semantic Versioning 2.0.0)
├── download_core.py        # yt-dlp options, playlist handling, history recording
├── history.py              # Download history (data/download_history.json)
├── logger.py               # Logging system
├── view_log.py             # Log viewing functionality
├── menu.py                 # User interface menu
├── help.py                 # Help system
├── about.py                # About information
├── sponsor.py              # Sponsor information
├── update.py               # Update system
├── ui/                     # PySide6 GUI
│   └── main_window.py     # Main window
├── lang/                   # Language system
│   ├── language_manager.py # Language management
│   └── translations.py    # Translation strings
├── docs/                   # Documentation
│   └── STRUCT.md          # This file
├── tests/                  # Test files (pytest)
├── assets/                 # Assets (images, icons, etc.)
├── README.md              # Project documentation
├── TO_DO.md               # To-do list
├── CHANGELOG.md           # Changelog
└── requirements.txt       # Python dependencies
```

## Module Descriptions

### Core Modules
- **main.py**: Main application entry point that handles URL input and video download
- **download_core.py**: yt-dlp logic shared by CLI and GUI (quality/format options, playlists, history recording)
- **history.py**: Persistent download history
- **logger.py**: Logging system for application events and errors
- **view_log.py**: Interface for viewing application logs

### UI Modules
- **menu.py**: User interface menu system
- **help.py**: Help system and documentation
- **about.py**: About information and credits
- **sponsor.py**: Sponsor and donation information

### System Modules
- **update.py**: Update checking and installation system
- **lang/language_manager.py**: Language management system
- **lang/translations.py**: Translation strings for supported languages

### Data
- **version.py**: Application version following Semantic Versioning 2.0.0
- **docs/**: Documentation files
- **tests/**: Test files using pytest
- **assets/**: Images, icons, and other assets

## Build System
- Python
- Black for code formatting
- Pytest for testing

## License
GPLv3
