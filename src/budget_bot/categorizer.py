"""Categorization utilities using OpenAI's API."""
from typing import Optional

from .config import OPENAI_API_KEY

import logging
import openai

# You need to set OPENAI_API_KEY environment variable

prompt_template = (
    "You are an assistant that categorizes expenses into "
    "broad categories such as groceries, entertainment, bills, gift, "
    "health, salary, etc.\n"
    "Given a short Russian description, return just the best category "
    "in English, e.g. 'groceries'."
)


if OPENAI_API_KEY:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
else:
    client = openai.OpenAI()


def categorize_description(description: str) -> Optional[str]:
    """Return a category for the description."""
    logging.info("Description to categorize: %s", description)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt_template},
                {"role": "user", "content": description},
            ],
            max_tokens=10,
        )
        logging.info("Response from OpenAI: %s", response)
        return response.choices[0].message.content.strip().lower()
    except Exception:
        logging.error("Error categorizing description", exc_info=True)
        return None
