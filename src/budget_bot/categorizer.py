"""Categorization utilities using OpenAI's API."""
from typing import Optional

import openai

# You need to set OPENAI_API_KEY environment variable

prompt_template = (
    "You are an assistant that categorizes expenses into "
    "broad categories such as groceries, entertainment, bills, gift, "
    "health, salary, etc.\n"
    "Given a short Russian description, return just the best category "
    "in English, e.g. 'groceries'."
)


def categorize_description(description: str) -> Optional[str]:
    """Return a category for the description."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt_template},
                {"role": "user", "content": description},
            ],
            max_tokens=10,
        )
        return response.choices[0].message["content"].strip().lower()
    except Exception:
        return None
