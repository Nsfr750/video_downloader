"""Tests for the logger module."""

import pytest
import sys
import os
import tempfile

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logger import VideoDownloaderLogger, get_logger, set_log_level


class TestVideoDownloaderLogger:
    """Test cases for VideoDownloaderLogger class."""

    @pytest.fixture
    def temp_log_dir(self):
        """Create a temporary directory for log files."""
        tmpdir = tempfile.mkdtemp()
        yield tmpdir
        # Clean up manually to avoid permission issues
        import shutil
        try:
            shutil.rmtree(tmpdir, ignore_errors=True)
        except:
            pass

    @pytest.fixture
    def logger(self, temp_log_dir):
        """Create a VideoDownloaderLogger instance for testing."""
        logger = VideoDownloaderLogger(log_dir=temp_log_dir)
        yield logger
        # Clean up handlers to release file locks
        for handler in logger.logger.handlers[:]:
            handler.close()
            logger.logger.removeHandler(handler)

    def test_init(self, logger, temp_log_dir):
        """Test logger initialization."""
        assert logger.log_dir == temp_log_dir
        assert logger.logger is not None
        assert os.path.exists(temp_log_dir)

    def test_info_logging(self, logger, caplog):
        """Test info level logging."""
        with caplog.at_level('INFO'):
            logger.info("Test info message")
            assert "Test info message" in caplog.text

    def test_error_logging(self, logger, caplog):
        """Test error level logging."""
        with caplog.at_level('ERROR'):
            logger.error("Test error message")
            assert "Test error message" in caplog.text

    def test_warning_logging(self, logger, caplog):
        """Test warning level logging."""
        with caplog.at_level('WARNING'):
            logger.warning("Test warning message")
            assert "Test warning message" in caplog.text

    def test_debug_logging(self, logger, caplog):
        """Test debug level logging."""
        # Set logger to DEBUG level
        logger.logger.setLevel(10)  # DEBUG level
        with caplog.at_level('DEBUG'):
            logger.debug("Test debug message")
            assert "Test debug message" in caplog.text

    def test_get_log_files_empty(self, logger):
        """Test getting log files when directory is empty (logger creates one log file)."""
        log_files = logger.get_log_files()
        # Logger creates one log file during initialization
        assert len(log_files) >= 1
        assert all(f.endswith('.log') for f in log_files)

    def test_get_log_files_with_logs(self, logger, temp_log_dir):
        """Test getting log files when logs exist."""
        # Create a test log file
        test_log = os.path.join(temp_log_dir, "test.log")
        with open(test_log, 'w') as f:
            f.write("test log content")

        log_files = logger.get_log_files()
        # Logger creates one log file during initialization, plus our test file
        assert len(log_files) >= 2
        assert test_log in log_files


class TestGlobalLogger:
    """Test cases for global logger functions."""

    def test_get_logger_singleton(self):
        """Test that get_logger returns the same instance."""
        logger1 = get_logger()
        logger2 = get_logger()
        assert logger1 is logger2

    def test_set_log_level(self):
        """Test setting log level."""
        import logging
        set_log_level(logging.DEBUG)
        logger = get_logger()
        assert logger.logger.level == logging.DEBUG
