# Playwright Python Quality Engineering Framework

[![Quality Engineering CI](https://github.com/PrashantSinghT99/playwright-ui-api-framework/actions/workflows/quality.yml/badge.svg)](https://github.com/PrashantSinghT99/playwright-ui-api-framework/actions/workflows/quality.yml)

A production-style UI, API, and cross-layer test automation framework built with Python,
Playwright, pytest, and typed executable contracts. It consolidates two earlier learning
repositories into one portfolio project designed to demonstrate senior SDET concerns:
architecture, risk-based coverage, test-data isolation, CI quality gates, observability, and
safe parallel execution.

The system under test is [Restful Booker Platform](https://github.com/mwinteringham/restful-booker-platform),
an open-source hotel-booking application created specifically for UI and API testing practice.
The public demo is the default target; any deployed copy can be selected through environment
configuration.

## What this demonstrates

| Capability | Implementation |
| --- | --- |
| UI automation | Playwright page objects with user-facing roles and labels |
| API automation | Playwright `APIRequestContext` with domain clients and Pydantic contracts |
| Cross-layer testing | Create through UI, observe and clean up through API |
| Environment management | Validated `.env` settings; no URLs or secrets inside tests |
| Parallel safety | Per-worker contexts and unique, recognizable synthetic data |
| Mutation safety | Data-changing tests skipped unless `--run-mutation` is explicit |
| Failure analysis | Retained-on-failure trace/video, screenshots, HTML and JUnit reports |
| Engineering gates | Ruff, strict mypy, pytest, coverage, locked dependencies, pip-audit, Dependabot |
| CI scale | Python matrix plus independently runnable API and browser jobs |

## Quick start

Python 3.11+ is required. Python 3.12 is the primary development version.

### Reproducible setup with uv

```bash
uv sync --extra dev
uv run playwright install chromium
uv run pytest -m smoke --browser chromium
```

The committed `uv.lock` resolves application and development dependencies to reviewed versions.
The standard `venv` and `pip` workflow remains available when `uv` is not installed.

### PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m playwright install chromium
Copy-Item .env.example .env
pytest -m smoke --browser chromium
```

### Bash

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
python -m playwright install chromium
cp .env.example .env
pytest -m smoke --browser chromium
```

## Common commands

```bash
# Fast deterministic feedback
pytest -m unit
ruff format --check .
ruff check .
mypy src

# Service and browser suites against the selected environment
pytest -m api -n auto
pytest -m ui --browser chromium
pytest -m smoke --browser chromium

# Full cross-browser check
pytest -m ui --browser chromium --browser firefox --browser webkit

# Data-changing CRUD and UI-to-API journeys (explicit opt-in)
pytest -m mutation --run-mutation --browser chromium

# Portable reports
pytest -m smoke --html=reports/smoke.html --self-contained-html \
  --junitxml=reports/smoke.xml
```

Playwright puts failure screenshots, videos, and trace archives in `test-results/`. Open a trace
with `playwright show-trace path/to/trace.zip`.

## Configuration

Copy `.env.example` to `.env`. Environment variables override file values.

| Variable | Default | Purpose |
| --- | --- | --- |
| `TEST_BASE_URL` | `https://automationintesting.online` | Target deployment origin |
| `TEST_ADMIN_USERNAME` | `admin` | Training-app administrator |
| `TEST_ADMIN_PASSWORD` | `password` | Training-app password |
| `TEST_ACTION_TIMEOUT_MS` | `10000` | Locator/action timeout |
| `TEST_NAVIGATION_TIMEOUT_MS` | `30000` | Navigation and API timeout |
| `TEST_EXPECT_TIMEOUT_MS` | `10000` | Assertion timeout budget |

The checked-in credentials are the public defaults documented by the open-source target. Use CI
secrets for non-public environments.

## Repository map

```text
src/quality_framework/
├── api/          # API routes, auth, diagnostics, executable contracts
├── data/         # Valid and parallel-safe domain test data
├── ui/           # Page objects exposing user/business behavior
└── config.py     # Validated environment settings
tests/
├── unit/         # No network or browser
├── api/          # Service and contract checks
├── ui/           # Browser behavior
└── e2e/          # Cross-layer journeys; mutation opt-in
docs/             # Architecture, test strategy, implementation, migration
legacy/           # Temporary review snapshot of the former learning tree
```

Framework-owned pytest fixtures are split across `src/quality_framework/pytest_plugins/`; the root
`tests/conftest.py` is intentionally only a small composition root.

Start with [the architecture](docs/ARCHITECTURE.md), then read the
[test strategy](docs/TEST_STRATEGY.md), [local target guide](docs/LOCAL_TARGET.md), and
[migration record](docs/MIGRATION.md). Contributors can follow the practical
[adding-a-test guide](docs/ADDING_A_TEST.md) for the supported extension patterns. The
[engineering decision log](DECISIONS.md) records the rationale and trade-offs behind the design.

## Companion technology stack

### [SauceDemo Automation Framework](https://github.com/PrashantSinghT99/selenium-java-automation)

A production-grade Selenium Java automation framework featuring both **Web UI** and **API** test
automation, built with industry best practices including Page Object Model, layered architecture,
parallel execution, and integrated reporting.

## Project history

This branch preserves both original repositories as parents in the Git graph. The former
`playwright-python` files are temporarily under `legacy/`; the former `api-playwright-python`
history remains directly accessible through Git. No generated reports or media are used by the
new framework.

## License

This framework is MIT licensed. Restful Booker Platform is a separate GPL-3.0 project and is not
redistributed here.
