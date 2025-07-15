from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Tuple

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from .data import load_data, save_data
from .categorizer import categorize_description
from .receipt import parse_receipt_image
from .utils import parse_expense_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Отправьте сумму и описание, например '20 продукты', "
        "или фото чека. Используйте /income <сумма> для добавления дохода, "
        "/stats для статистики."
    )


def add_expense(user_id: int, amount: float, desc: str, category: str) -> None:
    data = load_data()
    data["expenses"].append(
        {"user": user_id, "amount": amount, "desc": desc, "category": category}
    )
    save_data(data)


def add_income(user_id: int, amount: float, desc: str) -> None:
    data = load_data()
    data["incomes"].append({"user": user_id, "amount": amount, "desc": desc})
    save_data(data)


def compute_stats(user_id: int) -> str:
    data = load_data()
    incomes = sum(i["amount"] for i in data["incomes"] if i["user"] == user_id)
    expenses = [e for e in data["expenses"] if e["user"] == user_id]
    by_cat = {}
    for e in expenses:
        by_cat.setdefault(e["category"], 0)
        by_cat[e["category"]] += e["amount"]
    lines = [f"Доходы: {incomes:.2f}€"]
    total_expenses = sum(by_cat.values())
    lines.append(f"Расходы всего: {total_expenses:.2f}€")
    for cat, amt in by_cat.items():
        lines.append(f" - {cat}: {amt:.2f}€")
    lines.append(f"Итого: {incomes - total_expenses:.2f}€")
    return "\n".join(lines)


async def handle_income(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Используйте /income <сумма> <описание>")
        return
    try:
        amount = float(context.args[0].replace(",", "."))
    except ValueError:
        await update.message.reply_text("Не могу понять сумму")
        return
    desc = " ".join(context.args[1:]) or "income"
    add_income(update.effective_user.id, amount, desc)
    await update.message.reply_text("Доход добавлен")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    parsed = parse_expense_message(update.message.text)
    if not parsed:
        await update.message.reply_text(
            "Не могу понять сообщение. Напишите, например: '20 продукты'"
        )
        return
    amount, desc = parsed
    category = categorize_description(desc) or "other"
    add_expense(update.effective_user.id, amount, desc, category)
    await update.message.reply_text(
        f"Добавлено {amount:.2f}€ в категорию '{category}'"
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    photo = update.message.photo[-1]
    file = await photo.get_file()
    path = Path(f"/tmp/{file.file_id}.jpg")
    await file.download_to_drive(path)
    items = parse_receipt_image(path)
    if not items:
        await update.message.reply_text("Не удалось распознать чек")
        return
    for amount, desc in items:
        category = categorize_description(desc) or "other"
        add_expense(update.effective_user.id, amount, desc, category)
    await update.message.reply_text(f"Добавлено {len(items)} позиций из чека")
    path.unlink(missing_ok=True)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    report = compute_stats(update.effective_user.id)
    await update.message.reply_text(report)


def main() -> None:
    if not TOKEN:
        raise SystemExit("TELEGRAM_TOKEN environment variable not set")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("income", handle_income))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()


if __name__ == "__main__":
    main()
