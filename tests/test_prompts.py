import builtins
import json
from utils.prompts import ask_action, ask_ids_to_remove, ask_widgets_to_add


def test_ask_action_remove(monkeypatch):
    inputs = iter(["1"])  # remove
    monkeypatch.setattr(builtins, "input", lambda *args: next(inputs))
    assert ask_action() == "remove"


def test_ask_action_add(monkeypatch):
    inputs = iter(["2"])  # add
    monkeypatch.setattr(builtins, "input", lambda *args: next(inputs))
    assert ask_action() == "add"


def test_ask_ids_to_remove(monkeypatch):
    inputs = iter(["a,b , c "])
    monkeypatch.setattr(builtins, "input", lambda *args: next(inputs))
    assert ask_ids_to_remove() == ["a", "b", "c"]


def test_ask_widgets_to_add_valid(monkeypatch):
    payload = [{"id": "w1"}]
    inputs = iter(["anchor", json.dumps(payload)])
    monkeypatch.setattr(builtins, "input", lambda *args: next(inputs))
    spec = ask_widgets_to_add()
    assert spec["after_id"] == "anchor"
    assert spec["widgets"] == payload


def test_ask_widgets_to_add_invalid(monkeypatch, capsys):
    inputs = iter(["anchor", "not json"])
    monkeypatch.setattr(builtins, "input", lambda *args: next(inputs))
    spec = ask_widgets_to_add()
    assert spec["after_id"] == "anchor"
    assert spec["widgets"] == []
    out = capsys.readouterr().out
    assert "Неверный JSON" in out


