"""Main window for Video Downloader PySide6 GUI.

This module provides the graphical user interface for the video downloader application.
"""

import os
import sys
from typing import List, Optional
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTextEdit, QLabel, QProgressBar,
    QListWidget, QFileDialog, QComboBox, QTabWidget, QMessageBox,
    QGroupBox, QSplitter, QDialog
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QTextCursor, QPixmap
from logger import get_logger
from lang import get_language_manager, _
from version import __version__

COPYRIGHT = "© Copyright 2024-2026 Tuxxle - All rights reserved."

# Quality options mapping
QUALITY_OPTIONS = {
    'best': 'best',
    'worst': 'worst',
    '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
    '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
    '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
    '360p': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
    'audio': 'bestaudio/best',
}

# Format options mapping
FORMAT_OPTIONS = {
    'auto': None,
    'mp4': 'mp4',
    'webm': 'webm',
    'mkv': 'mkv',
    'avi': 'avi',
    'mp3': 'mp3',
    'm4a': 'm4a',
    'wav': 'wav',
}


class DownloadThread(QThread):
    """Thread for downloading videos to keep UI responsive."""
    
    progress_updated = Signal(str, float)  # url, percent
    download_complete = Signal(str, bool)   # url, success
    download_finished = Signal(int, int)    # successful, failed

    def __init__(self, urls: List[str], download_dir: str, quality: str = "best", format: str = "auto"):
        """Initialize download thread.

        Args:
            urls: List of URLs to download
            download_dir: Directory to save videos
            quality: Video quality (best, worst, 1080p, 720p, 480p, 360p, audio)
            format: Output format (auto, mp4, webm, mkv, avi, mp3, m4a, wav)
        """
        super().__init__()
        self.urls = urls
        self.download_dir = download_dir
        self.quality = quality
        self.format = format
        self.logger = get_logger()
        import yt_dlp
        self.yt_dlp = yt_dlp

    def run(self) -> None:
        """Run the download process."""
        successful = 0
        failed = 0

        for url in self.urls:
            try:
                self.logger.info(_('downloading').format(url=url))

                ydl_opts = {
                    'format': QUALITY_OPTIONS.get(self.quality, 'best'),
                    'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
                    'quiet': True,
                    'no_warnings': True,
                    'progress_hooks': [self._progress_hook],
                }

                # Add format conversion if specified
                if self.format != 'auto':
                    ydl_opts['merge_output_format'] = FORMAT_OPTIONS.get(self.format)

                with self.yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                self.logger.info(_('download_complete').format(url=url))
                self.download_complete.emit(url, True)
                successful += 1

            except Exception as e:
                self.logger.error(_('download_failed').format(url=url, error=str(e)))
                self.download_complete.emit(url, False)
                failed += 1

        self.download_finished.emit(successful, failed)

    def _progress_hook(self, d: dict) -> None:
        """Progress hook for download progress.
        
        Args:
            d: Dictionary containing download progress information
        """
        if d['status'] == 'downloading':
            try:
                percent_str = d.get('_percent_str', '0%').replace('%', '')
                percent = float(percent_str)
                self.progress_updated.emit(d.get('filename', ''), percent)
            except (ValueError, AttributeError):
                pass


class MainWindow(QMainWindow):
    """Main window for Video Downloader GUI."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.logger = get_logger()
        self.lang_manager = get_language_manager()
        self.download_dir = "downloads"
        self.quality = "best"
        self.format = "auto"
        self.urls: List[str] = []
        self.download_thread: Optional[DownloadThread] = None
        self.quality_group = None
        self.format_group = None
        self.quality_label = None
        self.format_label = None

        self._init_ui()
        self._update_language()

    def _init_ui(self) -> None:
        """Initialize the user interface."""
        self.setWindowTitle(_('app_title'))
        self.setMinimumSize(800, 600)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Create download tab
        self._create_download_tab()

        # Create logs tab
        self._create_logs_tab()

        # Create settings tab
        self._create_settings_tab()

        # Create status bar
        self.statusBar().showMessage(_('app_name'))

    def _create_download_tab(self) -> None:
        """Create the download tab."""
        download_tab = QWidget()
        layout = QVBoxLayout(download_tab)

        # URL input section
        url_group = QGroupBox(_('url_list'))
        url_layout = QVBoxLayout()

        # URL input field
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText(_('ui_url_placeholder'))
        url_layout.addWidget(self.url_input)

        # URL buttons
        url_button_layout = QHBoxLayout()
        self.add_url_button = QPushButton(_('ui_add_url'))
        self.add_url_button.clicked.connect(self._add_url)
        url_button_layout.addWidget(self.add_url_button)

        self.clear_urls_button = QPushButton(_('ui_clear_urls'))
        self.clear_urls_button.clicked.connect(self._clear_urls)
        url_button_layout.addWidget(self.clear_urls_button)

        url_layout.addLayout(url_button_layout)

        # URL list
        self.url_list = QListWidget()
        url_layout.addWidget(self.url_list)

        url_group.setLayout(url_layout)
        layout.addWidget(url_group)

        # Quality selection section
        quality_group = QGroupBox(_('quality_title'))
        quality_layout = QHBoxLayout()

        quality_label = QLabel(_('quality_select'))
        quality_layout.addWidget(quality_label)
        self.quality_label = quality_label

        self.quality_combo = QComboBox()
        self.quality_combo.addItem(_('quality_best'), 'best')
        self.quality_combo.addItem(_('quality_worst'), 'worst')
        self.quality_combo.addItem(_('quality_1080p_label'), '1080p')
        self.quality_combo.addItem(_('quality_720p_label'), '720p')
        self.quality_combo.addItem(_('quality_480p_label'), '480p')
        self.quality_combo.addItem(_('quality_360p_label'), '360p')
        self.quality_combo.addItem(_('quality_audio'), 'audio')
        self.quality_combo.setCurrentIndex(0)
        self.quality_combo.currentIndexChanged.connect(self._on_quality_changed)
        quality_layout.addWidget(self.quality_combo)

        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group)
        self.quality_group = quality_group

        # Format selection section
        format_group = QGroupBox(_('format_title'))
        format_layout = QHBoxLayout()

        format_label = QLabel(_('format_select'))
        format_layout.addWidget(format_label)
        self.format_label = format_label

        self.format_combo = QComboBox()
        self.format_combo.addItem(_('format_auto'), 'auto')
        self.format_combo.addItem(_('format_mp4'), 'mp4')
        self.format_combo.addItem(_('format_webm'), 'webm')
        self.format_combo.addItem(_('format_mkv'), 'mkv')
        self.format_combo.addItem(_('format_avi'), 'avi')
        self.format_combo.addItem(_('format_mp3'), 'mp3')
        self.format_combo.addItem(_('format_m4a'), 'm4a')
        self.format_combo.addItem(_('format_wav'), 'wav')
        self.format_combo.setCurrentIndex(0)
        self.format_combo.currentIndexChanged.connect(self._on_format_changed)
        format_layout.addWidget(self.format_combo)

        format_group.setLayout(format_layout)
        layout.addWidget(format_group)
        self.format_group = format_group

        # Download directory section
        dir_group = QGroupBox(_('ui_download_dir'))
        dir_layout = QHBoxLayout()

        self.dir_label = QLabel(self.download_dir)
        dir_layout.addWidget(self.dir_label)

        self.browse_button = QPushButton(_('ui_browse'))
        self.browse_button.clicked.connect(self._browse_directory)
        dir_layout.addWidget(self.browse_button)

        dir_group.setLayout(dir_layout)
        layout.addWidget(dir_group)

        # Download button
        self.download_button = QPushButton(_('ui_download'))
        self.download_button.clicked.connect(self._start_download)
        layout.addWidget(self.download_button)

        # Progress section
        progress_group = QGroupBox(_('ui_status'))
        progress_layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)

        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(150)
        progress_layout.addWidget(self.status_text)

        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        # Close button at bottom right
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        self.close_button = QPushButton(_('close'))
        self.close_button.setStyleSheet("background-color: #dc3545; color: white;")
        self.close_button.clicked.connect(self.close)
        close_layout.addWidget(self.close_button)
        layout.addLayout(close_layout)

        self.tab_widget.addTab(download_tab, _('menu_download'))

    def _create_logs_tab(self) -> None:
        """Create the logs tab."""
        logs_tab = QWidget()
        layout = QVBoxLayout(logs_tab)

        # Log viewer
        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)
        layout.addWidget(self.log_viewer)

        # Log buttons
        log_button_layout = QHBoxLayout()

        self.refresh_logs_button = QPushButton(_('ui_refresh_logs'))
        self.refresh_logs_button.clicked.connect(self._refresh_logs)
        log_button_layout.addWidget(self.refresh_logs_button)

        self.clear_logs_button = QPushButton(_('ui_clear_logs'))
        self.clear_logs_button.clicked.connect(self._clear_logs)
        log_button_layout.addWidget(self.clear_logs_button)

        layout.addLayout(log_button_layout)

        # Close button at bottom right
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        self.close_button_logs = QPushButton(_('close'))
        self.close_button_logs.setStyleSheet("background-color: #dc3545; color: white;")
        self.close_button_logs.clicked.connect(self.close)
        close_layout.addWidget(self.close_button_logs)
        layout.addLayout(close_layout)

        self.tab_widget.addTab(logs_tab, _('menu_view_logs'))

    def _create_settings_tab(self) -> None:
        """Create the settings tab."""
        settings_tab = QWidget()
        layout = QVBoxLayout(settings_tab)

        # Language selection
        lang_group = QGroupBox(_('ui_language'))
        lang_layout = QHBoxLayout()

        self.language_combo = QComboBox()
        languages = self.lang_manager.get_supported_languages()
        current_lang = self.lang_manager.get_language()

        for code, name in languages.items():
            self.language_combo.addItem(name, code)
            if code == current_lang:
                self.language_combo.setCurrentIndex(self.language_combo.count() - 1)

        self.language_combo.currentIndexChanged.connect(self._change_language)
        lang_layout.addWidget(self.language_combo)

        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)

        # Sponsor button
        self.sponsor_button = QPushButton(_('ui_sponsor'))
        self.sponsor_button.clicked.connect(self._show_sponsor)
        layout.addWidget(self.sponsor_button)

        # Update button
        self.update_button = QPushButton(_('ui_check_updates'))
        self.update_button.clicked.connect(self._check_updates)
        layout.addWidget(self.update_button)

        # About button
        self.about_button = QPushButton(_('menu_about'))
        self.about_button.clicked.connect(self._show_about)
        layout.addWidget(self.about_button)

        # Help button
        self.help_button = QPushButton(_('menu_help'))
        self.help_button.clicked.connect(self._show_help)
        layout.addWidget(self.help_button)

        layout.addStretch()

        # Close button at bottom right
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        self.close_button_settings = QPushButton(_('close'))
        self.close_button_settings.setStyleSheet("background-color: #dc3545; color: white;")
        self.close_button_settings.clicked.connect(self.close)
        close_layout.addWidget(self.close_button_settings)
        layout.addLayout(close_layout)

        self.tab_widget.addTab(settings_tab, _('menu_settings'))

    def _add_url(self) -> None:
        """Add URL to the list."""
        url = self.url_input.text().strip()
        if url:
            self.urls.append(url)
            self.url_list.addItem(url)
            self.url_input.clear()
        else:
            QMessageBox.warning(self, _('warning'), _('ui_no_urls_added'))

    def _clear_urls(self) -> None:
        """Clear all URLs from the list."""
        self.urls.clear()
        self.url_list.clear()

    def _browse_directory(self) -> None:
        """Browse for download directory."""
        directory = QFileDialog.getExistingDirectory(
            self, _('ui_select_dir'), self.download_dir
        )
        if directory:
            self.download_dir = directory
            self.dir_label.setText(directory)
            if not os.path.exists(directory):
                os.makedirs(directory)

    def _on_quality_changed(self, index: int) -> None:
        """Handle quality selection change.

        Args:
            index: Index of selected quality
        """
        self.quality = self.quality_combo.itemData(index)

    def _on_format_changed(self, index: int) -> None:
        """Handle format selection change.

        Args:
            index: Index of selected format
        """
        self.format = self.format_combo.itemData(index)

    def _start_download(self) -> None:
        """Start the download process."""
        if not self.urls:
            QMessageBox.warning(self, _('warning'), _('ui_no_urls_added'))
            return

        if self.download_thread and self.download_thread.isRunning():
            QMessageBox.information(self, _('info'), _('ui_downloading'))
            return

        self.download_button.setEnabled(False)
        self.status_text.clear()
        self.progress_bar.setValue(0)

        self.status_text.append(_('ui_download_started').format(count=len(self.urls)))

        self.download_thread = DownloadThread(self.urls, self.download_dir, self.quality, self.format)
        self.download_thread.progress_updated.connect(self._update_progress)
        self.download_thread.download_complete.connect(self._download_complete)
        self.download_thread.download_finished.connect(self._download_finished)
        self.download_thread.start()

    def _update_progress(self, filename: str, percent: float) -> None:
        """Update download progress.
        
        Args:
            filename: Name of the file being downloaded
            percent: Download progress percentage
        """
        self.progress_bar.setValue(int(percent))
        self.status_text.append(_('ui_progress').format(percent=percent))

    def _download_complete(self, url: str, success: bool) -> None:
        """Handle completion of a single download.
        
        Args:
            url: URL that was downloaded
            success: Whether the download was successful
        """
        status = _('ui_complete') if success else _('ui_failed')
        self.status_text.append(f"{url}: {status}")

    def _download_finished(self, successful: int, failed: int) -> None:
        """Handle completion of all downloads.
        
        Args:
            successful: Number of successful downloads
            failed: Number of failed downloads
        """
        self.download_button.setEnabled(True)
        self.progress_bar.setValue(100)

        summary = f"\n{'='*50}\n"
        summary += f"{_('ui_download_summary')}\n"
        summary += f"{'='*50}\n"
        summary += f"{_('ui_successful').format(count=successful)}\n"
        summary += f"{_('ui_failed_count').format(count=failed)}\n"
        summary += f"{'='*50}\n"
        self.status_text.append(summary)

        QMessageBox.information(
            self,
            _('ui_download_finished'),
            f"{_('ui_successful').format(count=successful)}\n{_('ui_failed_count').format(count=failed)}"
        )

    def _refresh_logs(self) -> None:
        """Refresh the log viewer."""
        try:
            log_file = os.path.join("logs", "app.log")
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    self.log_viewer.setText(f.read())
            else:
                self.log_viewer.setText(_('log_no_files'))
        except Exception as e:
            self.log_viewer.setText(f"{_('error')}: {str(e)}")

    def _clear_logs(self) -> None:
        """Clear the log file."""
        try:
            log_file = os.path.join("logs", "app.log")
            if os.path.exists(log_file):
                open(log_file, 'w').close()
                self.log_viewer.clear()
                QMessageBox.information(self, _('success'), _('success'))
        except Exception as e:
            QMessageBox.critical(self, _('error'), str(e))

    def _change_language(self, index: int) -> None:
        """Change the application language.
        
        Args:
            index: Index of the selected language
        """
        lang_code = self.language_combo.itemData(index)
        if self.lang_manager.set_language(lang_code):
            self._update_language()
            QMessageBox.information(
                self,
                _('success'),
                _('language_changed').format(self.language_combo.itemText(index))
            )

    def _update_language(self) -> None:
        """Update UI text with current language."""
        self.setWindowTitle(_('app_title'))
        self.tab_widget.setTabText(0, _('menu_download'))
        self.tab_widget.setTabText(1, _('menu_view_logs'))
        self.tab_widget.setTabText(2, _('menu_settings'))

        self.url_input.setPlaceholderText(_('ui_url_placeholder'))
        self.add_url_button.setText(_('ui_add_url'))
        self.clear_urls_button.setText(_('ui_clear_urls'))
        self.download_button.setText(_('ui_download'))
        self.dir_label.setText(self.download_dir)
        self.browse_button.setText(_('ui_browse'))
        self.refresh_logs_button.setText(_('ui_refresh_logs'))
        self.clear_logs_button.setText(_('ui_clear_logs'))
        self.sponsor_button.setText(_('ui_sponsor'))
        self.update_button.setText(_('ui_check_updates'))
        self.about_button.setText(_('menu_about'))
        self.help_button.setText(_('menu_help'))
        self.close_button.setText(_('close'))
        self.close_button_logs.setText(_('close'))
        self.close_button_settings.setText(_('close'))

        # Update quality and format group titles and labels
        if self.quality_group:
            self.quality_group.setTitle(_('quality_title'))
        if self.quality_label:
            self.quality_label.setText(_('quality_select'))
        if self.format_group:
            self.format_group.setTitle(_('format_title'))
        if self.format_label:
            self.format_label.setText(_('format_select'))

        # Update quality dropdown
        current_quality = self.quality_combo.currentData()
        self.quality_combo.clear()
        self.quality_combo.addItem(_('quality_best'), 'best')
        self.quality_combo.addItem(_('quality_worst'), 'worst')
        self.quality_combo.addItem(_('quality_1080p_label'), '1080p')
        self.quality_combo.addItem(_('quality_720p_label'), '720p')
        self.quality_combo.addItem(_('quality_480p_label'), '480p')
        self.quality_combo.addItem(_('quality_360p_label'), '360p')
        self.quality_combo.addItem(_('quality_audio'), 'audio')
        # Restore selection
        index = self.quality_combo.findData(current_quality)
        if index >= 0:
            self.quality_combo.setCurrentIndex(index)

        # Update format dropdown
        current_format = self.format_combo.currentData()
        self.format_combo.clear()
        self.format_combo.addItem(_('format_auto'), 'auto')
        self.format_combo.addItem(_('format_mp4'), 'mp4')
        self.format_combo.addItem(_('format_webm'), 'webm')
        self.format_combo.addItem(_('format_mkv'), 'mkv')
        self.format_combo.addItem(_('format_avi'), 'avi')
        self.format_combo.addItem(_('format_mp3'), 'mp3')
        self.format_combo.addItem(_('format_m4a'), 'm4a')
        self.format_combo.addItem(_('format_wav'), 'wav')
        # Restore selection
        index = self.format_combo.findData(current_format)
        if index >= 0:
            self.format_combo.setCurrentIndex(index)

    def _show_sponsor(self) -> None:
        """Show sponsor information dialog with QR code."""
        from sponsor import generate_monero_qrcode

        dialog = QDialog(self)
        dialog.setWindowTitle(_('sponsor_title'))
        dialog.setMinimumSize(600, 500)

        layout = QVBoxLayout()

        # PayPal section
        paypal_label = QLabel(_('paypal_label'))
        paypal_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(paypal_label)

        paypal_link = QLabel('<a href="https://paypal.me/3dmega">https://paypal.me/3dmega</a>')
        paypal_link.setOpenExternalLinks(True)
        layout.addWidget(paypal_link)

        layout.addSpacing(20)

        # Monero section
        monero_label = QLabel(_('monero_label'))
        monero_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(monero_label)

        # Generate and display QR code
        try:
            qr_path = generate_monero_qrcode()
            qr_pixmap = QPixmap(qr_path)
            if not qr_pixmap.isNull():
                qr_label = QLabel()
                qr_label.setPixmap(qr_pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                qr_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(qr_label)
            else:
                layout.addWidget(QLabel(_('qr_error_load')))
        except Exception as e:
            layout.addWidget(QLabel(_('qr_error_generate').format(error=str(e))))

        # Close button
        close_button = QPushButton(_('close'))
        close_button.setStyleSheet("background-color: #ff4444; color: white;")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec()

    def _check_updates(self) -> None:
        """Check for application updates."""
        from update import UpdateManager

        QMessageBox.information(self, _('update_title'), _('update_checking'))

        try:
            manager = UpdateManager()
            latest_version = manager.check_for_updates()
            if latest_version:
                comparison = manager._compare_versions(latest_version, __version__)
                if comparison > 0:
                    QMessageBox.information(
                        self,
                        _('update_title'),
                        _('update_available').format(latest_version)
                    )
                else:
                    QMessageBox.information(
                        self,
                        _('update_title'),
                        _('update_latest').format(__version__)
                    )
            else:
                QMessageBox.warning(
                    self,
                    _('update_title'),
                    _('update_error').format('Could not fetch version information')
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                _('update_title'),
                _('update_error').format(str(e))
            )

    def _show_about(self) -> None:
        """Show about dialog."""
        QMessageBox.about(self, _('about_title'), _('about_content').format(__version__))

    def _show_help(self) -> None:
        """Show help dialog."""
        QMessageBox.information(self, _('help_title'), _('help_content'))

    def closeEvent(self, event) -> None:
        """Handle close event.
        
        Args:
            event: Close event
        """
        if self.download_thread and self.download_thread.isRunning():
            reply = QMessageBox.information(
                self,
                _('warning'),
                _('ui_downloading'),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.download_thread.terminate()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def run_gui() -> None:
    """Run the GUI application."""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName(_('app_name'))
    app.setApplicationVersion(__version__)
    app.setOrganizationName('Tuxxle')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
