import os
import pytest

from ..app.services.extract import extract_action_items_llm


def test_extract_llm_bullet_list(monkeypatch):
    """LLM should return JSON list for bullet-style notes."""

    def fake_chat(model, messages):
        return {
            "message": {
                "content": '["Finish backend", "Write tests"]'
            }
        }

    monkeypatch.setattr("week2.app.services.extract.chat", fake_chat)

    text = """
    - Finish backend
    - Write tests
    """

    items = extract_action_items_llm(text)
    assert items == ["Finish backend", "Write tests"]


def test_extract_llm_keyword_lines(monkeypatch):
    """LLM should handle TODO/action prefixed lines."""

    def fake_chat(model, messages):
        return {
            "message": {
                "content": '["Submit assignment", "Email professor"]'
            }
        }

    monkeypatch.setattr("week2.app.services.extract.chat", fake_chat)

    text = """
    TODO: Submit assignment
    Action: Email professor
    """

    items = extract_action_items_llm(text)
    assert "Submit assignment" in items
    assert "Email professor" in items


def test_extract_llm_empty_input():
    """Empty input should return empty list."""
    items = extract_action_items_llm("")
    assert items == []


def test_extract_llm_invalid_json_fallback(monkeypatch):
    """If LLM output is invalid, fallback should not crash."""

    def fake_chat(model, messages):
        return {
            "message": {
                "content": "Not valid JSON output"
            }
        }

    monkeypatch.setattr("week2.app.services.extract.chat", fake_chat)

    text = "- Do something important"

    items = extract_action_items_llm(text)

    # Should fallback to heuristic extraction
    assert "Do something important" in items
