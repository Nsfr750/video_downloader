"""Tests for the sponsor module."""

import os
import sys
from unittest.mock import patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sponsor

MONERO_ADDRESS = (
    "47Jc6MC47WJVFhiQFYwHyBNQP5BEsjUPG6tc8R37FwcTY8K5Y3LvFzveSXoGiaDQSxDrnCUBJ5WBj6Fgmsfix8VPD4w3gXF"
)

requires_qr = pytest.mark.skipif(
    not sponsor.QR_AVAILABLE, reason="qrcode or ImageMagick (Wand) not available"
)


@pytest.fixture
def qr_dir(tmp_path):
    """Redirect the generated QR code to a temporary directory."""
    with patch("sponsor.tempfile.gettempdir", return_value=str(tmp_path)):
        yield tmp_path


class TestMoneroQrCode:
    """Test cases for Monero QR code generation."""

    def test_monero_address(self):
        """Test that the donation address is the expected one."""
        assert sponsor.MONERO_ADDRESS == MONERO_ADDRESS

    def test_generate_without_qr_support(self, qr_dir):
        """Test that no QR code is generated when the libraries are missing."""
        with patch("sponsor.QR_AVAILABLE", False):
            assert sponsor.generate_monero_qrcode() is None
        assert list(qr_dir.iterdir()) == []

    @requires_qr
    def test_generate_creates_png(self, qr_dir):
        """Test that a square PNG image is written to the temporary directory."""
        from wand.image import Image

        path = sponsor.generate_monero_qrcode()

        assert path == os.path.join(str(qr_dir), "monero_qrcode.png")
        assert os.path.isfile(path)
        with Image(filename=path) as img:
            assert img.format == "PNG"
            assert img.width == img.height
            assert img.width % sponsor.QR_BOX_SIZE == 0

    @requires_qr
    def test_generated_image_encodes_the_address(self, qr_dir):
        """Test that the image modules match the QR matrix of the address."""
        import qrcode
        from wand.image import Image

        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, border=4)
        qr.add_data(MONERO_ADDRESS)
        qr.make(fit=True)
        expected = [[bool(cell) for cell in row] for row in qr.get_matrix()]
        size = len(expected)

        with Image(filename=sponsor.generate_monero_qrcode()) as img:
            assert img.width == size * sponsor.QR_BOX_SIZE
            img.sample(size, size)
            pixels = img.export_pixels(channel_map="I", storage="char")

        actual = [
            [pixels[y * size + x] < 128 for x in range(size)] for y in range(size)
        ]
        assert actual == expected

    @requires_qr
    def test_generate_does_not_use_pillow(self, qr_dir):
        """Test that the QR code is rendered without the qrcode Pillow backend."""
        with patch("qrcode.QRCode.make_image") as mock_make_image:
            assert sponsor.generate_monero_qrcode() is not None
        mock_make_image.assert_not_called()


class TestDonationOptions:
    """Test cases for the CLI donation options."""

    def test_address_shown_without_qr_support(self, capsys):
        """Test that the text address is printed when no QR code can be made."""
        with patch("sponsor.QR_AVAILABLE", False):
            sponsor.show_donation_options()

        assert MONERO_ADDRESS in capsys.readouterr().out
