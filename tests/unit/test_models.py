from datetime import date

import pytest
from pydantic import ValidationError

from quality_framework.api.models import Booking, BookingDates, Room

pytestmark = pytest.mark.unit


def test_room_contract_maps_api_names_to_python_names() -> None:
    room = Room.model_validate(
        {
            "roomid": 1,
            "roomName": "101",
            "type": "Single",
            "accessible": True,
            "image": "/room.jpg",
            "description": "A room",
            "features": ["WiFi"],
            "roomPrice": 100,
        }
    )

    assert room.room_id == 1
    assert room.room_price == 100
    assert room.model_dump(by_alias=True)["roomName"] == "101"


def test_contract_rejects_unexpected_fields() -> None:
    with pytest.raises(ValidationError, match="unexpected"):
        Booking(
            roomid=1,
            firstname="AutoGuest",
            lastname="Example",
            depositpaid=False,
            bookingdates=BookingDates(checkin=date(2027, 1, 1), checkout=date(2027, 1, 3)),
            unexpected="drift",  # type: ignore[call-arg]
        )
