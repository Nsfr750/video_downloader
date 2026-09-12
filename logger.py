"""Logging system for Video Downloader application.

This module provides logging functionality for tracking application events,
errors, and user actions.
"""

import logging
import os
from datetime import datetime
from typing import Optional


class VideoDownloaderLogger:
    """Logger class for Video Downloader application."""

    def __init__(self, log_dir: str = "logs", log_level: int = logging.INFO):
        """Initialize the logger.

        Args:
            log_dir: Directory to store log files
            log_level: Logging level (default: INFO)
        """
        self.log_dir = log_dir
        self.log_level = log_level
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Set up the logger with file and console handlers.

        Returns:
            Configured logger instance
        """
        # Create logs directory if it doesn't exist
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Create logger
        logger = logging.getLogger("VideoDownloader")
        logger.setLevel(self.log_level)

        # Prevent duplicate handlers
        if logger.handlers:
            return logger

        # Create formatters
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_formatter = logging.Formatter(
            "%(levelname)s: %(message)s"
        )

        # File handler with date
        log_filename = f"video_downloader_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(
            os.path.join(self.log_dir, log_filename),
            encoding="utf-8"
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(file_formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(console_formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def info(self, message: str) -> None:
        """Log an info message.

        Args:
            message: Message to log
        """
        self.logger.info(message)

    def error(self, message: str) -> None:
        """Log an error message.

        Args:
            message: Error message to log
        """
        self.logger.error(message)

    def warning(self, message: str) -> None:
        """Log a warning message.

        Args:
            message: Warning message to log
        """
        self.logger.warning(message)

    def debug(self, message: str) -> None:
        """Log a debug message.

        Args:
            message: Debug message to log
        """
        self.logger.debug(message)

    def get_log_files(self) -> list[str]:
        """Get list of log files.

        Returns:
            List of log file paths
        """
        if not os.path.exists(self.log_dir):
            return []

        log_files = [
            os.path.join(self.log_dir, f)
            for f in os.listdir(self.log_dir)
            if f.endswith('.log')
        ]
        return sorted(log_files, reverse=True)


# Global logger instance
_logger_instance: Optional[VideoDownloaderLogger] = None


def get_logger() -> VideoDownloaderLogger:
    """Get the global logger instance.

    Returns:
        Global logger instance
    """
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = VideoDownloaderLogger()
    return _logger_instance


def set_log_level(level: int) -> None:
    """Set the logging level.

    Args:
        level: Logging level (logging.DEBUG, logging.INFO, etc.)
    """
    logger = get_logger()
    logger.logger.setLevel(level)
    for handler in logger.logger.handlers:
        handler.setLevel(level)
