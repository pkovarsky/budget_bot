import json
from pathlib import Path

import budget_bot.data as data


def test_load_defaults_and_save_creates_file(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    monkeypatch.setattr(data, "DATA_PATH", data_dir)
    monkeypatch.setattr(data, "DATA_FILE", data_dir / "budget.json")

    # File should not exist initially
    assert not data.DATA_FILE.exists()

    loaded = data.load_data()
    assert loaded == data.DEFAULT_DATA
    assert not data.DATA_FILE.exists()

    loaded["incomes"].append({"amount": 10})
    data.save_data(loaded)

    assert data.DATA_FILE.exists()
    with data.DATA_FILE.open("r", encoding="utf-8") as f:
        saved = json.load(f)
    assert saved == loaded
