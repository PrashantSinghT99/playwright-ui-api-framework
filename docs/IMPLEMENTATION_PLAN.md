# Implementation Plan

This is the execution plan used for the modernization. It is kept in the repository so future
changes can be evaluated against the original intent.

## Phase 1 — Repository consolidation

- Fetch both original repositories.
- Use `playwright-python` as the surviving history because it contains the broader learning path.
- Merge `api-playwright-python` as an unrelated-history parent so its commits remain discoverable.
- Work on `codex/modernize-ui-api-framework`; do not push or delete either remote automatically.
- Retain the former working tree in `legacy/` during review, then remove it in a dedicated approved
  cleanup commit.

## Phase 2 — Framework foundation

- Move packaging and tool configuration to `pyproject.toml`.
- Add immutable environment settings and documented defaults.
- Implement strict API contracts, a thin domain client, page objects, and test-data factories.
- Centralize resource ownership in pytest fixtures.

## Phase 3 — Risk-based portfolio

- Add deterministic framework unit tests.
- Add public-safe room, contract, negative-auth, and admin checks.
- Add browser smoke for discovery, price transparency, and authentication.
- Add opt-in, self-cleaning API CRUD and UI-to-API journeys.

## Phase 4 — Delivery engineering

- Add format, lint, type, unit, API, UI, and artifact CI jobs.
- Add dependency automation and pre-commit checks.
- Document architecture, strategy, migration, local execution, and resume narrative.

## Phase 5 — Verification and handoff

- Install the project in an isolated virtual environment.
- Install Chromium through Playwright.
- Run Ruff, mypy, pytest collection, unit, API, and UI smoke.
- Review all changes and confirm both histories remain reachable.
- Leave push, remote deletion, and permanent legacy-tree removal to an explicit user decision.
