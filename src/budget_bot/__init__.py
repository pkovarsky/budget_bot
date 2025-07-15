"""Expose convenience attributes lazily to avoid heavy imports."""

__all__ = [
    "load_data",
    "save_data",
    "DEFAULT_DATA",
    "parse_expense_message",
    "parse_receipt_image",
]


def __getattr__(name):
    if name in {"load_data", "save_data", "DEFAULT_DATA"}:
        from . import data
        return getattr(data, name)
    if name == "parse_expense_message":
        from . import utils
        return utils.parse_expense_message
    if name == "parse_receipt_image":
        from . import receipt
        return receipt.parse_receipt_image
    raise AttributeError(name)
