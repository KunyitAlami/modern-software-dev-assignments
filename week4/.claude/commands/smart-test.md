# /smart-test

Run backend tests in strict mode.

Steps:

1. Run: pytest -q backend/tests --maxfail=1 -x
2. If tests fail:
    - Summarize failures
    - Identify likely root cause
    - Suggest next debugging steps
3. If tests pass:
    - Run coverage report
    - Summarize coverage %
    - Flag files under 80%

Constraints:

- Do not modify files automatically
- Only suggest changes
