"""Executable API contracts for Restful Booker Platform."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class ContractModel(BaseModel):
    """Strict base model: unexpected response fields are contract drift."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class Room(ContractModel):
    room_id: PositiveInt = Field(alias="roomid")
    room_name: str = Field(alias="roomName", min_length=1)
    type: str = Field(min_length=1)
    accessible: bool
    image: str
    description: str
    features: list[str]
    room_price: PositiveInt = Field(alias="roomPrice")


class Rooms(ContractModel):
    rooms: list[Room]


class BookingDates(ContractModel):
    checkin: date
    checkout: date


class Booking(ContractModel):
    room_id: PositiveInt = Field(alias="roomid")
    firstname: str = Field(min_length=3, max_length=18)
    lastname: str = Field(min_length=3, max_length=30)
    deposit_paid: bool = Field(alias="depositpaid")
    booking_dates: BookingDates = Field(alias="bookingdates")
    email: str | None = None
    phone: str | None = None
    booking_id: PositiveInt | None = Field(default=None, alias="bookingid")


class Bookings(ContractModel):
    bookings: list[Booking]


class AuthToken(ContractModel):
    token: str = Field(min_length=1)


class ErrorResponse(ContractModel):
    error: str
