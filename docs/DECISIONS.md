# Engineering Decision Log

This log records the significant decisions made while consolidating and modernizing the original
Playwright Python UI and API repositories. It explains what was chosen, why it was chosen, what
changed, and which trade-offs remain. It is intentionally a decision record rather than a list of
commands or a resume narrative.

Unless noted otherwise, the decisions below were accepted and implemented during the modernization
session completed on 2026-08-16.

## D001 — Consolidate the UI and API repositories

**Decision:** Keep one Python repository containing UI, API, contract, unit, and cross-layer tests.

**Why:** The two former repositories demonstrated related capabilities but duplicated portfolio
space and did not show how a senior SDET would compose multiple test layers into one quality
strategy.

**Changes:**

- Used the former `playwright-python` repository as the surviving Git history.
- Merged the `api-playwright-python` history with an unrelated-history merge so its commits remain
  discoverable.
- Retained the former Playwright working tree temporarily under `legacy/` for review.
- Deleted the obsolete modernization branch after confirming its work was present on `master`.

**Trade-off:** The legacy snapshot creates noise in the main tree. It remains historical material,
not executable framework code, and is excluded from current quality tooling. It can later be
removed in a dedicated cleanup decision.

## D002 — Rename the surviving repository

**Decision:** Rename the project from the generic `playwright-python` to
`playwright-ui-api-framework`.

**Why:** The new name communicates the project’s combined UI/API purpose without implying that it
is an official Playwright repository.

**Changes:**

- Updated the Git remote to the renamed GitHub repository.
- Updated the README badge and package repository metadata.
- Preserved old repository names only where they describe migration history.

## D003 — Use a real open-source system under test

**Decision:** Automate the Restful Booker Platform at `https://automationintesting.online`.

**Why:** A portfolio framework should exercise a real browser application and real HTTP APIs. The
target is open source, contains connected hotel UI/API behavior, and is intended for automation
practice.

**Changes:**

- Configured the public deployment as the default target.
- Added support for selecting another deployment through environment variables.
- Added a helper and documentation for running a pinned upstream revision locally.

**Trade-off:** The public deployment is shared infrastructure and may drift or be temporarily
unavailable. Read-only smoke coverage can use it; mutation tests should prefer an owned target.

## D004 — Position the project as production-style, not production-proven

**Decision:** Describe the project as a production-style, scalable framework demonstration and
classify the package as Beta.

**Why:** The architecture demonstrates industry practices, but a portfolio target cannot provide
the business ownership, environment isolation, operational history, or regression breadth of a
company production system.

**Changes:**

- Kept the accurate `production-style` wording in the README.
- Changed the package classifier from `Production/Stable` to `Beta`.
- Removed resume-summary and interview-discussion sections from the README.

**Trade-off:** The project intentionally prioritizes representative architectural depth over claims
of enterprise operational maturity.

## D005 — Organize code by responsibility and domain

**Decision:** Separate configuration, API clients/contracts, UI page objects, test data, pytest
composition, and tests.

**Why:** Clear dependency boundaries make tests easier to extend and reduce the risk that junior
contributors place selectors, routes, credentials, or cleanup mechanics directly in tests.

**Changes:**

- Added the `src/quality_framework` package.
- Created dedicated `api`, `ui`, `data`, and `pytest_plugins` packages.
- Organized tests into `unit`, `api`, `ui`, and `e2e` suites.
- Documented allowed dependencies in `docs/ARCHITECTURE.md`.

**Trade-off:** The framework uses several small modules for clarity, but avoids additional service,
repository, workflow, or dependency-injection layers until real duplication justifies them.

## D006 — Use pytest fixtures as the composition mechanism

**Decision:** Provide settings, browser state, API contexts, authenticated clients, factories, and
cleanup ownership through pytest fixtures instead of test base classes or global singletons.

**Why:** Fixtures make dependencies visible in test signatures, provide lifecycle control, compose
cleanly across UI and API tests, and work naturally with pytest-xdist.

**Changes:**

- `api_client` is injected by pytest from a session-scoped Playwright `APIRequestContext`.
- `authenticated_api` composes authentication without modifying the unauthenticated client.
- Playwright supplies a new browser context and page for each UI test.
- Split the original large `tests/conftest.py` into focused framework-owned pytest plugins.
- Kept `tests/conftest.py` as a small plugin composition root.

**Trade-off:** Pytest plugin glue is excluded from the unit-only coverage gate because its lifecycle
is exercised by API and UI integration runs.

## D007 — Use Playwright for both browser and HTTP automation

**Decision:** Use Playwright `Page` for UI automation and `APIRequestContext` for API automation.

**Why:** One runtime provides consistent timeout behavior, lifecycle management, proxy support, and
diagnostics without adding another HTTP dependency only to increase the technology list.

**Changes:**

- Added a domain-focused `RestfulBookerApi` wrapper.
- Centralized paths, authentication cookies, and payload serialization in the client.
- Continued returning the original Playwright response so tests own expected statuses and business
  assertions.

**Trade-off:** The framework does not demonstrate the `requests` library, because it is unnecessary
for this system and would not improve the design.

## D008 — Use strict executable API contracts

**Decision:** Model important request and response payloads with strict Pydantic contracts.

**Why:** Typed contracts make wire-name translation explicit and cause unexpected response fields
or invalid domain data to fail visibly instead of drifting silently.

**Changes:**

- Added typed room, booking, authentication, and error models.
- Rejected unknown fields with `extra="forbid"`.
- Added a booking-date boundary requiring checkout to occur after check-in.
- Added unit coverage for aliases, drift detection, and date validation.

**Trade-off:** Strict contracts intentionally require review when the upstream API adds fields.

## D009 — Keep selectors and routes out of tests

**Decision:** Put user-facing browser behavior in page objects and HTTP routes in domain API
clients.

**Why:** Junior contributors should be able to read tests as behavior specifications and update one
location when UI selectors or API paths change.

**Changes:**

- Added page objects for the public home page, reservation page, and administrator login.
- Preferred accessible roles, labels, names, and web-first Playwright assertions.
- Added login rejection and logout behavior to the administrator page object.
- Added a contributor guide with canonical API, UI, mutation, and E2E examples.

**Trade-off:** Page objects expose behavior rather than implementing a generic browser-action
utility library.

## D010 — Make configuration explicit and validated

**Decision:** Load URLs, credentials, and timeout budgets through immutable Pydantic settings.

**Why:** Environment-specific values should not be embedded in tests, and invalid configuration
should fail at startup rather than during a test.

**Changes:**

- Added `.env` support with `TEST_` environment-variable overrides.
- Validated the base URL and positive timeout values.
- Applied action and navigation timeouts to pages.
- Applied `TEST_EXPECT_TIMEOUT_MS` once per pytest worker to Playwright assertions.

## D011 — Generate recognizable, parallel-safe test data

**Decision:** Generate valid booking objects with a short UUID fingerprint and future booking dates.

**Why:** Unique data prevents tests from relying on shared names or record order and makes created
records recognizable in UI, API responses, logs, and cleanup diagnostics.

**Changes:**

- Added `BookingFactory` using Faker plus UUID-derived values.
- Added a `future_stay` fixture.
- Removed the UI test’s hard-coded room ID and nightly price; it now discovers room data through the
  real API before asserting the UI quote.

**Trade-off:** Safe tests are parallel-isolated. Mutation tests still share the target’s rooms and
date namespace, so fully concurrent mutation execution should use worker-specific date allocation
or a controlled worker count on an owned target.

## D012 — Make mutation explicit and cleanup idempotent

**Decision:** Skip data-changing tests unless `--run-mutation` is supplied and register created IDs
for cleanup.

**Why:** The default target is public and shared. A safe default prevents accidental data pollution,
while explicit mutation coverage still demonstrates CRUD and cross-layer lifecycle design.

**Changes:**

- Added the `mutation` marker and collection-time opt-in policy.
- Added booking cleanup in reverse creation order.
- Treated HTTP `200`, `202`, `204`, and `404` as successful idempotent cleanup outcomes.
- Kept API CRUD and UI-created booking E2E tests opt-in.

**Trade-off:** Mutation tests are intentionally excluded from normal public-target CI.

## D013 — Retry only eventual consistency

**Decision:** Use a small polling helper only where a UI-created booking may take time to become
observable through the API.

**Why:** A fixed sleep either wastes time or remains flaky. Broad test retries can hide defects,
whereas bounded polling describes the specific consistency boundary.

**Changes:**

- Replaced the E2E test’s fixed sleep loop with `poll_until`.
- Added unit coverage for transient absence and diagnostic timeout behavior.
- Did not add automatic failed-test reruns.

## D014 — Demonstrate representative real coverage, not test volume

**Decision:** Cap the suite at a small set of high-value examples. The implemented suite contains 28
collected tests.

**Why:** The objective is to demonstrate risk-based architecture and maintainable patterns, not to
simulate a complete hotel regression pack or inflate test count.

**Changes:**

- Covered authentication, authorization, rooms, response contracts, reservation pricing, CRUD,
  UI-to-API persistence, framework logic, and cleanup.
- Added invalid administrator login and logout UI scenarios.
- Added unauthenticated booking-detail coverage.
- Recorded the upstream unknown-room `500` response as a strict known-defect `xfail` against the
  desired `404` behavior.

**Trade-off:** Many possible product cases are deliberately absent. A real product team would add
coverage from its own risk model and production defects.

## D015 — Support parallel execution without shared browser state

**Decision:** Make safe API and UI tests compatible with pytest-xdist and isolated Playwright
contexts.

**Why:** Parallel execution is a realistic scalability concern, while shared pages, global clients,
or ordered tests create state leakage.

**Changes:**

- Added `pytest-xdist` and documented `-n auto` execution.
- Created one session API context per xdist worker process.
- Used a fresh browser context/page per UI test.
- Generated unique booking identities and avoided test ordering.
- Ran the API and complete safe suite successfully with eight workers during verification.

**Trade-off:** The default UI CI smoke remains simple, and parallel mutation execution is not
claimed against the shared public environment.

## D016 — Use lightweight, portable failure evidence

**Decision:** Use Playwright-native traces, screenshots, and video together with HTML and JUnit
reports.

**Why:** These artifacts are portable, work in CI, and provide the evidence needed to distinguish
product, contract, environment, and automation failures without operating a separate reporting
server.

**Changes:**

- Retain trace, screenshot, and video only on failures.
- Publish HTML, JUnit, coverage, and Playwright artifacts from GitHub Actions.
- Include the selected target URL in the pytest report header.

**Trade-off:** Allure and external observability platforms were deliberately excluded because they
would add operational complexity without proving a new design capability in this demo.

## D017 — Enforce reproducible and secure-enough dependencies

**Decision:** Keep project metadata in `pyproject.toml`, commit `uv.lock`, and run a lightweight
dependency vulnerability audit.

**Why:** Version ranges make the package reusable, while a lockfile makes local and CI verification
reproducible. A portfolio CI pipeline should also demonstrate basic software-supply-chain hygiene.

**Changes:**

- Added and verified `uv.lock`.
- Updated CI to use `uv sync --locked --extra dev`.
- Added `pip-audit`; the verified environment reported no known dependency vulnerabilities.
- Retained Dependabot for Python and GitHub Actions updates.

**Trade-off:** The framework does not add a full software-composition-analysis platform or multiple
overlapping security scanners.

## D018 — Use proportionate CI quality gates

**Decision:** Keep separate quality, API, and UI jobs with a Python-version matrix and selectable
browser, rather than building a complex deployment platform.

**Why:** The workflow should demonstrate pipeline strategy, parallel API execution, quality gates,
and artifact publication while remaining understandable to a reviewer.

**Changes:**

- Added Ruff format/lint, strict mypy, unit coverage, and dependency-audit gates.
- Added Python 3.11, 3.12, and 3.13 quality verification.
- Added parallel API/contract execution.
- Added Chromium UI smoke with manual Firefox/WebKit selection.
- Added concurrency cancellation, job timeouts, least-privilege permissions, and artifact uploads.

**Trade-off:** Scheduled mutation deployment, multi-tenant provisioning, test-management publishing,
and distributed browser infrastructure are outside this demo’s scope.

## D019 — Keep the Python and Java portfolios complementary

**Decision:** Mention the separate Selenium Java UI/API framework as a companion technology stack
instead of merging Java and Python into one repository.

**Why:** The two projects demonstrate different ecosystems. Combining languages would obscure the
Python framework’s structure, while a concise cross-reference shows breadth without duplicating
resume space.

**Changes:** Added the SauceDemo Selenium Java framework link and description to the README.

## D020 — Deliberately exclude unnecessary portfolio features

**Decision:** Stop implementation when each senior-SDET concern has a representative example.

**Why:** Architectural restraint is itself a test-architect skill. Features should solve observed
problems rather than exist only to lengthen a technology list.

**Deliberate exclusions:**

- BDD/Cucumber and custom test DSLs;
- test base classes, global browser singletons, and ordered tests;
- generic UI action wrappers and deep inheritance;
- database, Kubernetes, or cloud infrastructure unrelated to the target;
- visual-regression, load-testing, and external observability platforms;
- blind retries and automatic flaky-test reruns;
- dozens of repetitive tests;
- additional abstraction layers without demonstrated duplication.

## Verification record

The final uncommitted modernization work was verified with:

- 28 tests collected;
- 25 tests passed;
- 2 mutation tests skipped by the safety policy;
- 1 strict known-defect `xfail`;
- 13 unit tests passed;
- 89.17% branch-aware core coverage;
- Ruff format and lint passed;
- strict mypy passed across 19 source files;
- all pre-commit hooks passed;
- the dependency lock passed its consistency check;
- `pip-audit` found no known dependency vulnerabilities;
- the complete safe suite passed using pytest-xdist with eight workers and Chromium.

This verification describes the state at the end of the recorded session. Future changes should
update this log only when they introduce or reverse a significant engineering decision.

## Upcoming commit coverage map

This map accounts for every modified or new file planned for the modernization commit. It exists
to make clear which decision authorized each change; it is not a substitute for the detailed
rationale above.

| Files | Change represented | Decisions |
| --- | --- | --- |
| `.github/workflows/quality.yml` | Locked CI installation, vulnerability audit, and quality/API/UI jobs | D017, D018 |
| `.pre-commit-config.yaml` | Exclude the read-only legacy snapshot from current hooks | D001 |
| `README.md` | Correct repository badge, locked setup, framework map, contributor and decision links | D002, D004, D005, D017, D019 |
| `docs/ARCHITECTURE.md` | Document focused pytest plugins and lifecycle responsibilities | D005, D006, D012 |
| `docs/MIGRATION.md` | Reflect the renamed surviving repository | D001, D002 |
| `docs/TEST_STRATEGY.md` | Add lock and vulnerability-audit exit criteria | D017, D018 |
| `docs/ADDING_A_TEST.md` | Give juniors canonical API, UI, mutation, and E2E extension patterns | D005, D009, D012, D014 |
| `pyproject.toml` | Beta classification, correct repository URL, audit dependency, and coverage boundaries | D002, D004, D006, D017 |
| `uv.lock` | Reproducible application and development dependency resolution | D017 |
| `src/quality_framework/pytest_plugins/*` | Separate policy, configuration, browser, API, and data fixture ownership | D006, D010, D012, D015 |
| `tests/conftest.py` | Reduce the root conftest to a plugin composition root | D006 |
| `src/quality_framework/api/models.py` | Enforce the check-in/check-out domain boundary | D008 |
| `tests/unit/test_models.py` | Verify date-boundary contract behavior | D008, D014 |
| `src/quality_framework/ui/admin_login_page.py` | Model login rejection and actual logout redirect behavior | D009, D014 |
| `tests/ui/test_admin_login.py` | Exercise successful login, invalid login, and logout through the real UI | D003, D009, D014 |
| `tests/ui/test_reservation.py` | Discover room ID and price through the API before validating the UI quote | D003, D011, D014 |
| `tests/api/test_auth_api.py` | Verify unauthenticated booking detail is rejected with HTTP 403 | D007, D014 |
| `tests/api/test_rooms_api.py` | Record unknown-room HTTP 500 as a strict expected defect against desired HTTP 404 | D008, D014 |
| `src/quality_framework/polling.py` | Provide one bounded eventual-consistency primitive | D013 |
| `tests/unit/test_polling.py` | Verify polling recovery and timeout diagnostics | D013, D014 |
| `tests/e2e/test_booking_journey.py` | Replace fixed sleeping with bounded polling at the UI-to-API boundary | D012, D013 |
| `docs/DECISIONS.md` | Preserve the session’s decisions, rationale, trade-offs, verification, and commit map | D001–D020 |
