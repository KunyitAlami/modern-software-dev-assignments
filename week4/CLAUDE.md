# Claude Repository Guide — Week 4

## Project Overview

Minimal full-stack developer command center.

Backend:

- FastAPI app in backend/
- Routers: backend/app/routers
- Models: backend/app/models
- Tests: backend/tests
- Database seed: data/

Frontend:

- Static files served by FastAPI

## Development Workflow (Test-First Policy)

When implementing a new feature:

1. Write a failing test first in backend/tests/.
2. Run tests:
   make test
3. Implement minimal code to pass the test.
4. Run:
   make format
   make lint
   make test

Never skip lint/test validation.

## Tooling Rules

- Code must pass black formatting.
- Code must pass ruff lint.
- Do not modify database schema without updating models.
- Avoid destructive shell commands.

## Safe Commands

- make run
- make test
- make format
- make lint

## Expected Behavior

When asked to:

- Add endpoint → write failing test first
- Refactor module → run lint + tests after
- Update API → ensure /docs still works

Always summarize what files were modified.
