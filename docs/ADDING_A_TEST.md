# Adding a Test

This guide defines the shortest supported path for extending the framework. Tests should describe
product behavior; selectors, routes, credentials, serialization, and cleanup belong in their
respective framework layers.

## Choose the cheapest effective layer

| Behavior | Preferred layer |
| --- | --- |
| Pure configuration, model, factory, or client logic | Unit |
| HTTP behavior, authorization, validation, or response compatibility | API/contract |
| Rendering, navigation, accessibility, or browser interaction | UI |
| A business outcome that must cross UI and API boundaries | E2E |

Keep E2E coverage intentionally small. A behavior that can be proven through an API test should
not be repeated through the browser without a user-facing risk that justifies it.

## API test pattern

Request the domain client by fixture name. The client owns the route and transport behavior; the
test owns the expected status, contract, and business assertion.

```python
import pytest

from quality_framework.api import RestfulBookerApi, expect_status
from quality_framework.api.models import Rooms

pytestmark = [pytest.mark.api, pytest.mark.contract]


def test_rooms_have_unique_identifiers(api_client: RestfulBookerApi) -> None:
    response = expect_status(api_client.get_rooms(), 200)
    rooms = Rooms.model_validate(response.json()).rooms

    assert len({room.room_id for room in rooms}) == len(rooms)
```

When an endpoint is missing, add it to the appropriate domain client. Do not place `/api/...`
routes directly in a test.

## UI test pattern

Page objects expose business behavior and web-first assertions. Tests do not contain selectors.

```python
import pytest
from playwright.sync_api import Page

from quality_framework.config import Settings
from quality_framework.ui import HomePage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_guest_can_open_the_hotel(page: Page, settings: Settings) -> None:
    home = HomePage(page, settings)

    home.open()

    home.expect_loaded()
```

Prefer roles, labels, accessible names, and stable domain language. Add a component object when a
UI region such as navigation or a form is reused across multiple pages.

## Mutation and cleanup pattern

Every test that changes target data must use the `mutation` marker and register the created ID as
soon as it becomes available.

```python
@pytest.mark.mutation
def test_booking_can_be_created(
    api_client: RestfulBookerApi,
    booking_cleanup: list[int],
) -> None:
    response = expect_status(api_client.create_booking(booking), 201)
    booking_id = find_created_booking_id()
    booking_cleanup.append(booking_id)

    # Continue with assertions after cleanup ownership is registered.
```

Mutation tests are skipped unless `--run-mutation` is supplied. Run them against an owned local
target whenever possible.

## Cross-layer E2E pattern

Use the API for fast observation and cleanup, while keeping the behavior under test in the UI:

1. Discover isolated input data through the API.
2. Perform the user journey through a page object.
3. Poll only the eventual-consistency boundary.
4. Validate the persisted domain object through a typed API contract.
5. Register the resource for API cleanup.

Do not put API clients inside page objects. Cross-layer orchestration stays visible in the test or
in a small domain workflow when several tests require the same setup behavior.

## Definition of done

Before opening a pull request:

```bash
ruff format .
ruff check .
mypy src
pytest -m unit
pytest --collect-only -q
```

Also run the smallest relevant real suite, for example `pytest -m api` or
`pytest -m "ui and smoke" --browser chromium`. A new test is complete when it is independent,
parallel-safe, marked correctly, produces useful failure evidence, and updates documentation when
it introduces a new setting or execution mode.
