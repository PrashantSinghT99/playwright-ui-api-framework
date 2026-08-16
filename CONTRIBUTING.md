# Contributing

1. Create a branch from the modern default branch.
2. Install `.[dev]` and Chromium in a virtual environment.
3. Keep selectors/routes inside page objects or API clients.
4. Mark data-changing coverage with `mutation` and register cleanup immediately.
5. Run `ruff format .`, `ruff check .`, `mypy src`, and `pytest -m unit` before opening a pull
   request.
6. Include failure evidence and the target environment when reporting flakes or defects.

Tests must be independently runnable. Do not add ordering, fixed sleeps in page objects, committed
artifacts, real credentials, or broad exception handling that hides failures.
