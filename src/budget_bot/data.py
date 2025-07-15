import json
from pathlib import Path
from typing import Any, Dict, List

DATA_PATH = Path(__file__).resolve().parent.parent / "data"
DATA_FILE = DATA_PATH / "budget.json"

DEFAULT_DATA = {"incomes": [], "expenses": []}


def load_data() -> Dict[str, Any]:
    DATA_PATH.mkdir(exist_ok=True)
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_DATA.copy()


def save_data(data: Dict[str, Any]) -> None:
    DATA_PATH.mkdir(exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
