from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
import openai

# Load environment variables from .env located at project root
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
