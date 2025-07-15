import re
from typing import Optional, Tuple


AMOUNT_RE = re.compile(r"(?P<amount>\d+[\.,]?\d*)\s+(?P<desc>.+)")


def parse_expense_message(text: str) -> Optional[Tuple[float, str]]:
    """Parse messages like '20 продукт' and return amount and description."""
    m = AMOUNT_RE.match(text.strip())
    if not m:
        return None
    amount_str = m.group("amount").replace(",", ".")
    try:
        amount = float(amount_str)
    except ValueError:
        return None
    description = m.group("desc").strip()
    return amount, description
