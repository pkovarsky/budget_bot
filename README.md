# Budget Bot

Телеграм-бот для учёта доходов и расходов.

## Возможности

- Добавление расходов простым сообщением вида `20 продукты`.
- Загрузка фотографий чеков для автоматического распознавания.
- Добавление доходов командой `/income <сумма> <описание>`.
- Получение статистики командой `/stats`.
- Категоризация расходов осуществляется через ChatGPT.

## Запуск

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Для распознавания чеков установите Tesseract OCR и русские языковые данные. Например, в Debian/Ubuntu выполните:
   ```bash
   sudo apt install tesseract-ocr tesseract-ocr-rus
   ```
3. Скопируйте файл `.env.example` в `.env` и заполните в нём `TELEGRAM_TOKEN` и
   `OPENAI_API_KEY`.
4. Запустите бота:

   ```bash
   cd src && python -m budget_bot.bot
   ```
   или из корня проекта, указав путь к модулям:
   ```bash
   PYTHONPATH=src python -m budget_bot.bot
   ```
