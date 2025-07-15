"""Receipt parsing utilities."""
from pathlib import Path
from typing import List

from PIL import Image
import pytesseract

from .utils import parse_expense_message


def parse_receipt_image(path: Path) -> List[tuple[float, str]]:
    """Extract expenses from a receipt image."""
    text = pytesseract.image_to_string(Image.open(path), lang="rus")
    items: List[tuple[float, str]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parsed = parse_expense_message(line)
        if parsed:
            items.append(parsed)
    return items
