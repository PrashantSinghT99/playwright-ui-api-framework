# Test Strategy

## Product risk model

Restful Booker Platform is a hotel-booking system with public discovery/reservation flows and an
authenticated administration surface. The framework focuses on risks that transfer well to
industry systems:

| Risk | Cheapest effective layer | Example coverage |
| --- | --- | --- |
| Deployment unavailable or core data missing | API smoke | room collection is healthy and non-empty |
| Breaking response drift | API contract | strict room/booking models |
| Authentication bypass/regression | API + UI | protected route rejects guest; admin signs in |
| Price misleading before purchase | UI | nightly rate, fees, and total are itemized |
| Booking lost between layers | Cross-layer | create in UI, query and clean through API |
| CRUD behavior broken | API mutation | create, read, update, delete lifecycle |

## Suite taxonomy

- `unit`: framework logic only; required on every pull request.
- `api`: fast service checks; suitable after each deployment.
- `contract`: strict compatibility checks, normally a subset of API.
- `ui`: user-visible behavior in an isolated browser context.
- `smoke`: minimal confidence set spanning API and UI.
- `mutation`: changes target data and is skipped unless `--run-mutation` is supplied.
- `e2e`: crosses architectural boundaries; keep this set intentionally small.

Markers describe why and where a test runs. They do not encode test order or priority.

## Pipeline recommendation

| Stage | Selection | Browser | Mutation | Failure policy |
| --- | --- | --- | --- | --- |
| Pull request | `unit` + lint + type-check | none | off | blocks merge |
| Deployment smoke | `smoke` | Chromium | off | blocks promotion |
| Component regression | `api or ui` | Chromium | off | blocks release |
| Nightly owned environment | all | Chromium/Firefox/WebKit | on | triage next business day |

The checked-in GitHub workflow demonstrates the first three. Mutation tests are manual by default
because the public training deployment is shared.

## Test design rules

1. Assert one coherent behavior, with multiple checks only when they diagnose the same outcome.
2. Use APIs for setup and cleanup when the behavior under test is UI-only.
3. Generate data per test; never depend on the public seed record remaining unchanged.
4. Locate UI through accessible roles, labels, and stable domain language.
5. Assert response status before parsing its body.
6. Parse important responses through strict contracts.
7. Keep retry logic at eventual-consistency boundaries only, never around arbitrary failed tests.
8. Quarantine only with an issue, owner, evidence, and expiry date; do not use blind reruns.

## Parallelism and isolation

pytest-xdist starts a separate Python process and therefore a separate session API context per
worker. Playwright creates a new browser context for every test. Test data uses unique names and
future dates. Mutation tests register created IDs immediately so teardown can recover from later
assertion failures.

If a target environment cannot provide independent tenant/database isolation, mutation workers
should be capped or allocated distinct rooms/tenants by CI rather than forcing serial ordering into
test code.

## Failure evidence

The default pytest configuration retains trace, video, and screenshot artifacts only for failures.
CI also publishes HTML, JUnit XML, and the complete `test-results` directory. The first triage pass
should answer:

1. Did the request reach the intended environment?
2. Was the failure product behavior, contract drift, target availability, or test logic?
3. Does the Playwright trace show a product/network/console error before the assertion?
4. Is cleanup needed for a mutation test?

## Exit criteria for framework changes

- Ruff format and lint pass.
- Strict mypy passes for framework code.
- Unit suite passes without network access.
- API and UI tests collect without warnings.
- At least Chromium smoke is exercised against a known target.
- New data-changing behavior is marked `mutation` and registers cleanup.
- Documentation and `.env.example` reflect new settings or commands.
