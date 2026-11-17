"""Update system for Video Downloader application.

This module provides functionality to check for and install updates.
"""

import json
import urllib.request
from typing import Optional
from logger import get_logger
from lang import _
from version import __version__

COPYRIGHT = "© Copyright 2024-2026 Tuxxle - All rights reserved."

# GitHub repository information
GITHUB_REPO = "Nsfr750/video_downloader"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


class UpdateManager:
    """Update manager class for Video Downloader application."""

    def __init__(self):
        """Initialize the update manager."""
        self.logger = get_logger()

    def check_for_updates(self) -> Optional[str]:
        """Check for available updates.

        Returns:
            Latest version string if available, None if error occurred
        """
        try:
            self.logger.info("Checking for updates...")

            # Fetch latest release information from GitHub
            with urllib.request.urlopen(GITHUB_API_URL, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))

            latest_version = data.get('tag_name', '').lstrip('v')

            if latest_version:
                self.logger.info(f"Latest version: {latest_version}")
                self.logger.info(f"Current version: {__version__}")

            return latest_version

        except urllib.error.HTTPError as e:
            if e.code == 404:
                self.logger.info("No releases found on GitHub (repository may not have any releases yet)")
            else:
                self.logger.error(f"HTTP error checking for updates: {e}")
            return None
        except urllib.error.URLError as e:
            self.logger.error(f"Network error checking for updates: {e}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing update information: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error checking for updates: {e}")
            return None

    def _compare_versions(self, version1: str, version2: str) -> int:
        """Compare two version strings.

        Args:
            version1: First version string
            version2: Second version string

        Returns:
            1 if version1 > version2, -1 if version1 < version2, 0 if equal
        """
        v1_parts = [int(x) for x in version1.split('.')]
        v2_parts = [int(x) for x in version2.split('.')]

        # Pad with zeros if needed
        max_len = max(len(v1_parts), len(v2_parts))
        v1_parts.extend([0] * (max_len - len(v1_parts)))
        v2_parts.extend([0] * (max_len - len(v2_parts)))

        for v1, v2 in zip(v1_parts, v2_parts):
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1

        return 0

    def get_release_notes(self) -> Optional[str]:
        """Get release notes for the latest version.

        Returns:
            Release notes string, or None if unavailable
        """
        try:
            with urllib.request.urlopen(GITHUB_API_URL, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))

            return data.get('body', 'No release notes available.')

        except Exception as e:
            self.logger.error(f"Error fetching release notes: {e}")
            return None

    def download_update(self) -> bool:
        """Download the latest update.

        Returns:
            True if download was successful, False otherwise
        """
        try:
            self.logger.info("Downloading update...")

            with urllib.request.urlopen(GITHUB_API_URL, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))

            # Get download URL for the latest release
            assets = data.get('assets', [])
            if not assets:
                self.logger.error("No download assets found in release")
                return False

            download_url = assets[0].get('browser_download_url')
            if not download_url:
                self.logger.error("No download URL found")
                return False

            # Download the file
            filename = assets[0].get('name', 'update.zip')
            self.logger.info(f"Downloading {filename}...")

            with urllib.request.urlopen(download_url, timeout=30) as response:
                with open(filename, 'wb') as f:
                    f.write(response.read())

            self.logger.info(f"Update downloaded: {filename}")
            return True

        except Exception as e:
            self.logger.error(f"Error downloading update: {e}")
            return False


def check_for_updates() -> Optional[str]:
    """Check for updates using the global update manager.

    Returns:
        Latest version string if update is available, None otherwise
    """
    manager = UpdateManager()
    return manager.check_for_updates()


def get_release_notes() -> Optional[str]:
    """Get release notes using the global update manager.

    Returns:
        Release notes string, or None if unavailable
    """
    manager = UpdateManager()
    return manager.get_release_notes()


if __name__ == "__main__":
    print(f"\n{'='*50}")
    print(f"{_('update_title')}")
    print(f"{'='*50}")
    print(f"{_('update_checking')}")

    manager = UpdateManager()
    latest_version = manager.check_for_updates()

    if latest_version:
        print(f"\n{_('update_available').format(latest_version)}")

        notes = manager.get_release_notes()
        if notes:
            print(f"\nRelease Notes:")
            print("-" * 50)
            print(notes)
            print("-" * 50)
    else:
        print(f"\n{_('update_latest').format(__version__)}")

    print(f"{'='*50}\n")
