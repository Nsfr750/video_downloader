# Video Downloader

A Python application for downloading videos from the internet using yt-dlp.

## Features

- Download videos from multiple URLs
- Support for various video platforms (YouTube, Vimeo, etc.)
- Multi-language support (English, Italian, Spanish, French, German)
- Quality selection (best, worst, 1080p, 720p, 480p, 360p, audio)
- Format conversion (auto, mp4, webm, mkv, avi, mp3, m4a, wav)
- Logging system
- Easy-to-use interface
- Graphical User Interface (GUI) with PySide6
- Command Line Interface (CLI) mode
- QR code for Monero donations

## Requirements

- Python 3.13 or higher
- yt-dlp
- Wand
- PySide6
- pytest (for testing)

## Installation

```bash
py -3.13 -m pip install -r requirements.txt
```

Or if Python 3.13 is your default:

```bash
pip install -r requirements.txt
```

**Note**: Use `py -3.13` to ensure Python 3.13 is used for all commands.

## Usage

### GUI Mode (Default)

```bash
py -3.13 main.py
```

Or explicitly:

```bash
py -3.13 main.py --gui
```

### CLI Mode

```bash
py -3.13 main.py --cli
```

## Configuration

- Language system in `lang/` folder
- Logging system in `logger.py`
- Menu system in `menu.py`
- GUI system in `ui/` folder

## Security

For security reports, please contact: info@tuxxle.org

See [SECURITY.md](SECURITY.md) for more information.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Copyright
© Copyright 2024-2026 Tuxxle - All rights reserved.

## Author

- **Nsfr750** - [GitHub](https://github.com/Nsfr750)
- **Website**: https://www.tuxxle.org
- **Email**: nsfr750@yandex.com
- **Security Report**: info@tuxxle.org

## Sponsor

Support the project:
- **PayPal**: [https://paypal.me/3dmega](https://paypal.me/3dmega)
- **Monero**: 47Jc6MC47WJVFhiQFYwHyBNQP5BEsjUPG6tc8R37FwcTY8K5Y3LvFzveSXoGiaDQSxDrnCUBJ5WBj6Fgmsfix8VPD4w3gXF

## Organization

**Tuxxle**
