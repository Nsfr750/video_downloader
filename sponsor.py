"""Sponsor information for Video Downloader application.

This module provides information about how to support the project.
"""

import os
import tempfile
from typing import Optional
from lang import _

try:
    import qrcode
    from wand.color import Color
    from wand.drawing import Drawing
    from wand.image import Image
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False


MONERO_ADDRESS = "47Jc6MC47WJVFhiQFYwHyBNQP5BEsjUPG6tc8R37FwcTY8K5Y3LvFzveSXoGiaDQSxDrnCUBJ5WBj6Fgmsfix8VPD4w3gXF"
QR_BOX_SIZE = 10


def generate_monero_qrcode() -> Optional[str]:
    """Generate QR code for Monero address.

    The QR matrix is computed by qrcode and rendered with Wand.

    Returns:
        Path to the generated QR code image, or None if qrcode/Wand is not available
    """
    if not QR_AVAILABLE:
        return None

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        border=4,
    )
    qr.add_data(MONERO_ADDRESS)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    size = len(matrix)

    qr_path = os.path.join(tempfile.gettempdir(), "monero_qrcode.png")
    with Image(width=size, height=size, background=Color("white")) as img:
        with Drawing() as draw:
            draw.fill_color = Color("black")
            for y, row in enumerate(matrix):
                for x, dark in enumerate(row):
                    if dark:
                        draw.point(x, y)
            draw(img)
        img.sample(size * QR_BOX_SIZE, size * QR_BOX_SIZE)
        img.format = "png"
        img.save(filename=qr_path)

    return qr_path


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
    """)

    # Generate and display QR code if available
    if QR_AVAILABLE:
        try:
            qr_path = generate_monero_qrcode()
            print(f"QR Code saved to: {qr_path}")
            print("Scan the QR code below to donate Monero:")

            # Open the QR code image with default image viewer
            if os.name == 'nt':  # Windows
                os.startfile(qr_path)
            elif os.name == 'posix':  # Linux/Mac
                import subprocess
                if 'darwin' in os.uname().sysname.lower():  # macOS
                    subprocess.run(['open', qr_path])
                else:  # Linux
                    subprocess.run(['xdg-open', qr_path])

            print("\nPrivacy-focused cryptocurrency")
            print("No transaction fees for the developer")
        except Exception as e:
            print(f"Error generating QR code: {e}")
            print(f"Monero Address: {MONERO_ADDRESS}")
    else:
        print(f"Monero Address: {MONERO_ADDRESS}")
        print("(QR code generation not available - qrcode module not installed)")

    print("""
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
