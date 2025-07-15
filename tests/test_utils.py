from budget_bot.utils import parse_expense_message


def test_parse_expense_message_simple():
    assert parse_expense_message("20 продукты") == (20.0, "продукты")


def test_parse_expense_message_decimal_comma():
    assert parse_expense_message("15,5 подарок") == (15.5, "подарок")


def test_parse_expense_message_invalid():
    assert parse_expense_message("просто текст") is None
