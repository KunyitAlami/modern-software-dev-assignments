from backend.app.services.extract import extract_action_items


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "ACTION: review PR" in items
    assert "Ship it!" in items


def test_extract_with_deadline():
    text = "Finish report by Friday"
    result = extract_action_items(text)
    assert "Finish report by Friday" in result


def test_extract_with_modal_verbs():
    text = "We should fix this bug"
    result = extract_action_items(text)
    assert "We should fix this bug" in result