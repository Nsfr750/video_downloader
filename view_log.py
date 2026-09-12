"""Log viewing functionality for Video Downloader application.

This module provides functionality to view and display application logs.
"""

import os
from typing import Optional
from logger import get_logger
from lang import _


class LogViewer:
    """Log viewer class for displaying application logs."""

    def __init__(self):
        """Initialize the log viewer."""
        self.logger = get_logger()

    def display_latest_log(self, lines: int = 50) -> None:
        """Display the latest log file content.

        Args:
            lines: Number of lines to display from the end of the file
        """
        log_files = self.logger.get_log_files()

        if not log_files:
            print("No log files found.")
            return

        latest_log = log_files[0]
        self._display_log_file(latest_log, lines)

    def display_specific_log(self, log_file: str, lines: int = 50) -> None:
        """Display a specific log file content.

        Args:
            log_file: Path to the log file
            lines: Number of lines to display from the end of the file
        """
        if not os.path.exists(log_file):
            print(f"Log file not found: {log_file}")
            return

        self._display_log_file(log_file, lines)

    def _display_log_file(self, log_file: str, lines: int) -> None:
        """Display log file content.

        Args:
            log_file: Path to the log file
            lines: Number of lines to display from the end of the file
        """
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()

            print(f"\n{'='*60}")
            print(f"Log file: {log_file}")
            print(f"Total lines: {len(all_lines)}")
            print(f"{'='*60}\n")

            # Display last N lines
            display_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            for line in display_lines:
                print(line.rstrip())

            print(f"\n{'='*60}\n")

        except Exception as e:
            print(f"Error reading log file: {e}")

    def list_log_files(self) -> None:
        """List all available log files."""
        log_files = self.logger.get_log_files()

        if not log_files:
            print("No log files found.")
            return

        print("\nAvailable log files:")
        print("-" * 60)
        for i, log_file in enumerate(log_files, 1):
            size = os.path.getsize(log_file)
            print(f"{i}. {log_file} ({size} bytes)")
        print("-" * 60 + "\n")

    def clear_logs(self) -> None:
        """Clear all log files."""
        log_files = self.logger.get_log_files()

        if not log_files:
            print("No log files to clear.")
            return

        for log_file in log_files:
            try:
                os.remove(log_file)
                print(f"Deleted: {log_file}")
            except Exception as e:
                print(f"Error deleting {log_file}: {e}")

        print("All log files cleared.")


def view_logs_menu() -> None:
    """Display the log viewing menu."""
    viewer = LogViewer()

    while True:
        print(f"\n=== {_('log_title')} ===")
        print("1. View latest log")
        print("2. List all log files")
        print("3. Clear all logs")
        print("4. Back to main menu")
        print("-" * 20)

        choice = input(_("enter_your_choice")).strip()

        if choice == "1":
            viewer.display_latest_log()
        elif choice == "2":
            viewer.list_log_files()
        elif choice == "3":
            confirm = input("Are you sure you want to clear all logs? (y/n): ").strip().lower()
            if confirm == 'y':
                viewer.clear_logs()
        elif choice == "4":
            break
        else:
            print(_("invalid_choice"))


if __name__ == "__main__":
    view_logs_menu()
