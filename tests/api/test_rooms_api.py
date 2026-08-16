from datetime import date

import pytest

from quality_framework.api import RestfulBookerApi, expect_status
from quality_framework.api.models import Room, Rooms

pytestmark = [pytest.mark.api, pytest.mark.contract]


@pytest.mark.smoke
def test_rooms_response_matches_contract(api_client: RestfulBookerApi) -> None:
    response = expect_status(api_client.get_rooms(), 200)

    rooms = Rooms.model_validate(response.json()).rooms

    assert rooms, "Expected the environment to expose at least one room"
    assert all(room.room_price > 0 for room in rooms)
    assert len({room.room_id for room in rooms}) == len(rooms)


def test_room_detail_agrees_with_room_collection(api_client: RestfulBookerApi) -> None:
    rooms = Rooms.model_validate(expect_status(api_client.get_rooms(), 200).json()).rooms

    detail = Room.model_validate(expect_status(api_client.get_room(rooms[0].room_id), 200).json())

    assert detail == rooms[0]


def test_room_filter_accepts_a_stay_window(
    api_client: RestfulBookerApi,
    future_stay: tuple[date, date],
) -> None:
    response = expect_status(api_client.get_rooms(*future_stay), 200)

    Rooms.model_validate(response.json())


@pytest.mark.xfail(
    reason="known target defect: an unknown room currently returns 500 instead of 404",
    strict=True,
)
def test_unknown_room_returns_not_found(api_client: RestfulBookerApi) -> None:
    expect_status(api_client.get_room(2_147_483_647), 404)
