from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters

def extract_action_items_llm(text: str) -> List[str]:
    """
    Extract action items using an LLM via Ollama.

    Returns:
        List[str]: a list of extracted action items.
    """

    if not text.strip():
        return []

    model_name = os.getenv("OLLAMA_MODEL", "llama3.1:8b")


    prompt = f"""
You are an assistant that extracts action items from notes.

Return ONLY a valid JSON array of strings.
Each string should be one clear action item.

Notes:
{text}

Output format example:
["Do the homework", "Email the professor"]
"""

    try:
        response = chat(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        content = response["message"]["content"].strip()

        # Try to extract JSON substring
        start = content.find("[")
        end = content.rfind("]")

        if start == -1 or end == -1:
            return extract_action_items(text)

        json_str = content[start:end + 1]

        action_items = json.loads(json_str)

        if not isinstance(action_items, list):
            return extract_action_items(text)

        cleaned = [
            str(item).strip()
            for item in action_items
            if isinstance(item, str) and item.strip()
        ]

        return cleaned


    except Exception as e:
        print("LLM extraction failed:", e)

        # Fallback to heuristic extraction
        return extract_action_items(text)
