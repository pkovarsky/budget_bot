import sys
import types

# Provide a fake openai module before importing the module under test
fake_openai = types.ModuleType("openai")
fake_openai.OpenAI = lambda *args, **kwargs: None
sys.modules.setdefault("openai", fake_openai)

import budget_bot.categorizer as categorizer

class FakeResponse:
    def __init__(self, content):
        msg = types.SimpleNamespace(content=content)
        self.choices = [types.SimpleNamespace(message=msg)]

def test_categorize_description(monkeypatch):
    class FakeClient:
        def __init__(self):
            self.chat = types.SimpleNamespace(
                completions=types.SimpleNamespace(create=self.create)
            )

        def create(self, *args, **kwargs):
            return FakeResponse("groceries")

    monkeypatch.setattr(categorizer, "client", FakeClient())
    assert categorizer.categorize_description("20 продукты") == "groceries"

def test_categorize_description_error(monkeypatch):
    class ErrorClient:
        def __init__(self):
            self.chat = types.SimpleNamespace(
                completions=types.SimpleNamespace(create=self.create)
            )

        def create(self, *args, **kwargs):
            raise RuntimeError("boom")

    monkeypatch.setattr(categorizer, "client", ErrorClient())
    assert categorizer.categorize_description("20 продукты") is None
