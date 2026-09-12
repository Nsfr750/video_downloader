"""Sponsor information for Video Downloader application.

This module provides information about how to support the project.
"""

from lang import _


def show_sponsor() -> None:
    """Display sponsor information."""
    print(f"\n{'='*50}")
    print(f"{_('sponsor_title')}")
    print(f"{'='*50}")
    print(_('sponsor_content'))
    print(f"{'='*50}\n")


def show_donation_options() -> None:
    """Display detailed donation options."""
    print(f"\n{'='*50}")
    print("Donation Options")
    print(f"{'='*50}")
    print("""
Support the development of Video Downloader

PayPal:
- Link: https://paypal.me/3dmega
- Fast and secure
- Supports multiple currencies

Monero (XMR):
- Address: 47Jc6MC47WJVFhiQFYwHyBNQP5BEsjUPG6tc8R37FwcTY8K5Y3LvFzveSXoGiaDQSxDrnCUBJ5WBj6Fgmsfix8VPD4w3gXF
- Privacy-focused cryptocurrency
- No transaction fees for the developer

Why donate?
- Support ongoing development
- Help cover server costs
- Enable new features
- Keep the project free and open-source

Every donation is greatly appreciated!
    """)
    print(f"{'='*50}\n")


def show_patreon_alternatives() -> None:
    """Display alternative support methods."""
    print(f"\n{'='*50}")
    print("Other Ways to Support")
    print(f"{'='*50}")
    print("""
If you can't donate financially, you can still support the project:

1. Star the repository on GitHub
2. Report bugs and issues
3. Suggest new features
4. Help with translations
5. Share the project with others
6. Write reviews and feedback
7. Contribute code (if you're a developer)

Community support is just as valuable as financial support!
    """)
    print(f"{'='*50}\n")


if __name__ == "__main__":
    show_sponsor()
    show_donation_options()
    show_patreon_alternatives()
