"""Menu system for Video Downloader application.

This module provides the user interface menu system.
"""

from typing import Optional
from logger import get_logger
from lang import get_language_manager, _


class Menu:
    """Menu class for Video Downloader application."""

    def __init__(self):
        """Initialize the menu."""
        self.logger = get_logger()
        self.lang_manager = get_language_manager()

    def show_main_menu(self) -> None:
        """Display the main menu."""
        while True:
            print(f"\n{'='*50}")
            print(f"{_('menu_title')}")
            print(f"{'='*50}")
            print(f"1. {_('menu_download')}")
            print(f"2. {_('menu_view_logs')}")
            print(f"3. {_('menu_language')}")
            print(f"4. {_('menu_help')}")
            print(f"5. {_('menu_about')}")
            print(f"6. {_('menu_update')}")
            print(f"7. {_('menu_history')}")
            print(f"8. {_('menu_exit')}")
            print(f"{'='*50}")

            choice = input(_("enter_your_choice")).strip()

            if choice == "1":
                self.download_menu()
            elif choice == "2":
                self.view_logs_menu()
            elif choice == "3":
                self.language_menu()
            elif choice == "4":
                self.show_help()
            elif choice == "5":
                self.show_about()
            elif choice == "6":
                self.check_updates()
            elif choice == "7":
                self.history_menu()
            elif choice == "8":
                print(f"\n{_('app_name')} - {_('close')}")
                break
            else:
                print(_("invalid_choice"))

    def download_menu(self) -> None:
        """Display the download menu."""
        from main import VideoDownloader

        print(f"\n{'='*50}")
        print(f"{_('menu_download')}")
        print(f"{'='*50}")

        downloader = VideoDownloader()
        quality = downloader.select_quality()
        downloader.quality = quality
        format = downloader.select_format()
        downloader.format = format
        downloader.playlist = downloader.select_playlist()
        urls = downloader.get_urls_from_user()
        downloader.download_videos(urls)

    def history_menu(self, limit: int = 20) -> None:
        """Display the most recent downloads and allow clearing the history.

        Args:
            limit: Maximum number of downloads to show
        """
        from history import get_history
        from main import is_yes

        history = get_history()
        entries = history.get_entries(limit=limit)

        print(f"\n{'='*50}")
        print(f"{_('menu_history')}")
        print(f"{'='*50}")

        if not entries:
            print(_('history_empty'))
            print(f"{'='*50}\n")
            input(_("press_enter_continue"))
            return

        for i, entry in enumerate(entries, 1):
            status = _('history_status_completed') if entry.completed else _('history_status_failed')
            date = entry.timestamp.replace('T', ' ')
            print(f"{i}. [{date}] {status} - {entry.title or entry.url} ({entry.quality}, {entry.format})")
            if entry.title:
                print(f"   {entry.url}")
            if entry.file_path:
                print(f"   {entry.file_path}")
            if entry.error:
                print(f"   {_('error')}: {entry.error}")

        print(f"{'='*50}")
        print(f"1. {_('history_clear')}")
        print(f"2. {_('back')}")
        print(f"{'='*50}")

        choice = input(_("enter_your_choice")).strip()
        if choice == "1" and is_yes(input(_('history_clear_confirm') + _('yes_no_hint'))):
            history.clear()
            print(f"\n{_('history_cleared')}")

    def view_logs_menu(self) -> None:
        """Display the logs viewing menu."""
        from view_log import view_logs_menu
        view_logs_menu()

    def language_menu(self) -> None:
        """Display the language selection menu."""
        print(f"\n{'='*50}")
        print(f"{_('language_title')}")
        print(f"{'='*50}")

        languages = self.lang_manager.get_supported_languages()
        current_lang = self.lang_manager.get_language()

        for i, (code, name) in enumerate(languages.items(), 1):
            marker = " <--" if code == current_lang else ""
            print(f"{i}. {name}{marker}")

        print(f"{'='*50}")

        choice = input(_("enter_your_choice")).strip()

        try:
            choice_num = int(choice)
            lang_codes = list(languages.keys())

            if 1 <= choice_num <= len(lang_codes):
                selected_lang = lang_codes[choice_num - 1]
                if self.lang_manager.set_language(selected_lang):
                    print(f"\n{_('language_changed').format(languages[selected_lang])}")
                else:
                    print(f"\n{_('error')}: Failed to change language")
            else:
                print(_("invalid_choice"))
        except ValueError:
            print(_("invalid_choice"))

    def show_help(self) -> None:
        """Display help information."""
        print(f"\n{'='*50}")
        print(f"{_('help_title')}")
        print(f"{'='*50}")
        print(_('help_content'))

        from help import show_troubleshooting, show_usage_guide

        while True:
            print(f"{'='*50}")
            print(f"1. {_('usage_title')}")
            print(f"2. {_('troubleshooting_title')}")
            print(f"3. {_('back')}")
            print(f"{'='*50}")

            choice = input(_("enter_your_choice")).strip()
            if choice == "1":
                show_usage_guide()
            elif choice == "2":
                show_troubleshooting()
            else:
                break

    def show_about(self) -> None:
        """Display about information."""
        from version import __version__

        print(f"\n{'='*50}")
        print(f"{_('about_title')}")
        print(f"{'='*50}")
        print(_('about_content').format(__version__))
        print(f"{'='*50}\n")

        input(_("press_enter_continue"))

    def show_sponsor(self) -> None:
        """Display sponsor information."""
        print(f"\n{'='*50}")
        print(f"{_('sponsor_title')}")
        print(f"{'='*50}")
        print(_('sponsor_content'))
        print(f"{'='*50}\n")

        input(_("press_enter_continue"))

    def check_updates(self) -> None:
        """Check for application updates."""
        from version import __version__
        from update import UpdateManager

        print(f"\n{'='*50}")
        print(f"{_('update_title')}")
        print(f"{'='*50}")
        print(f"{_('update_checking')}")

        try:
            manager = UpdateManager()
            latest_version = manager.check_for_updates()
            if latest_version:
                comparison = manager._compare_versions(latest_version, __version__)
                if comparison > 0:
                    print(f"\n{_('update_available').format(latest_version)}")
                else:
                    print(f"\n{_('update_latest').format(__version__)}")
            else:
                print(f"\n{_('update_error').format('Could not fetch version information')}")
        except Exception as e:
            print(f"\n{_('update_error').format(str(e))}")

        print(f"{'='*50}\n")

        input(_("press_enter_continue"))


def show_main_menu() -> None:
    """Show the main menu."""
    menu = Menu()
    menu.show_main_menu()


if __name__ == "__main__":
    show_main_menu()
