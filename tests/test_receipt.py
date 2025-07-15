import sys
import types
from pathlib import Path

# Provide stub modules so receipt can be imported without real dependencies
fake_pytesseract = types.ModuleType("pytesseract")
fake_pytesseract.image_to_string = lambda img, lang=None: ""
sys.modules.setdefault("pytesseract", fake_pytesseract)

fake_pil = types.ModuleType("PIL")
class FakeImage:
    @staticmethod
    def open(path):
        return path
fake_pil.Image = FakeImage
sys.modules.setdefault("PIL", fake_pil)

import budget_bot.receipt as receipt


def test_parse_receipt_image(monkeypatch, tmp_path):
    sample_text = "20 продукты\n15,5 подарок\nнеподходящая строка"
    monkeypatch.setattr(
        receipt.pytesseract,
        "image_to_string",
        lambda *args, **kwargs: sample_text,
    )
    monkeypatch.setattr(receipt, "Image", FakeImage)

    path = tmp_path / "dummy.png"
    result = receipt.parse_receipt_image(path)
    assert result == [(20.0, "продукты"), (15.5, "подарок")]
