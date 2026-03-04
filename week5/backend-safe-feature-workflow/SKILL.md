---
name: backend-safe-feature-workflow
description: >
  Reusable backend development workflow for a FastAPI + SQLAlchemy project under week5/.
  Use this skill whenever implementing, modifying, or extending backend features including
  routes, Pydantic schemas, response models, or tests. Triggers on any backend feature work
  such as adding endpoints, changing API shape, updating models, or fixing backend bugs.
---

# Backend Safe Feature Workflow

Iterative develop-lint-test loop for the FastAPI backend in `week5/`.

## Project Layout

```
week5/
  backend/
    app/
      main.py            # FastAPI app, exception handler
      models.py          # SQLAlchemy models (Note, ActionItem)
      schemas.py         # Pydantic schemas + SuccessResponse[T], ErrorResponse
      db.py              # Engine, get_db dependency
      utils/responses.py # success() / error() envelope helpers
      routers/
        notes.py         # /notes CRUD + search + pagination
        action_items.py  # /action-items CRUD + complete + pagination
      services/
        extract.py       # extract_action_items()
    tests/
      conftest.py        # client fixture (temp SQLite)
      test_notes.py
      test_action_items.py
      test_extract.py
```

## Constraints

- Only modify files inside `week5/`.
- Never delete existing tests.
- All responses use the envelope helpers in `backend/app/utils/responses.py`:
  - Success: `{"ok": true, "data": ...}`
  - Error: `{"ok": false, "error": {"code": "...", "message": "..."}}`
- Paginated list endpoints return `data` as: `{"items": [...], "total": N, "page": N, "page_size": N}`.
- Pydantic schemas live in `backend/app/schemas.py`. Keep `SuccessResponse[T]` and `ErrorResponse` unchanged.

## Workflow Steps

Execute these steps in order for every backend change:

### 1. Implement the Feature

- Add or modify routes in `backend/app/routers/`.
- Add or modify SQLAlchemy models in `backend/app/models.py`.
- Add or modify service logic in `backend/app/services/`.

### 2. Update Schemas

If the API shape changed:

- Add or update Pydantic models in `backend/app/schemas.py`.
- Ensure new read schemas set `class Config: from_attributes = True`.
- Use `SuccessResponse[T]` as `response_model` on every endpoint.

### 3. Update Tests

If the API shape changed:

- Update assertions in existing tests to match the new response shape.
- Add new test functions for new endpoints.
- Never remove existing test functions.
- Tests use the `client` fixture from `conftest.py` (temp SQLite DB, auto-cleanup).

### 4. Format and Lint (run from `week5/`)

```
black .
ruff check . --fix
```

Fix any remaining lint errors that `--fix` cannot auto-resolve.

### 5. Run Tests

```
pytest -q backend/tests
```

### 6. Fix Failures

If any test fails:

1. Read the traceback carefully.
2. Fix the source code (not the test) first. Only update a test if the new API shape is intentionally different.
3. Return to Step 4 and repeat.

### 7. Loop Until Green

Repeat Steps 4-6 until `pytest` reports all tests passing with exit code 0.

## Checklist Before Done

- All tests pass.
- `black .` produces no changes.
- `ruff check .` reports no errors.
- Response envelopes are consistent with the existing pattern.