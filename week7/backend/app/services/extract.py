import re


ACTION_KEYWORDS = [
    r"^todo:",
    r"^action:",
    r"\bshould\b",
    r"\bmust\b",
    r"\bneed to\b",
    r"\bhave to\b",
    r"\bby\s+\w+",       
    r"\bbefore\s+\w+",   
]


def extract_action_items(text: str) -> list[str]:
    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    results: list[str] = []

    for line in lines:
        normalized = line.lower()

        matched = any(re.search(pattern, normalized) for pattern in ACTION_KEYWORDS)

        if matched or line.endswith("!"):
            if line not in results:
                results.append(line)

    return results