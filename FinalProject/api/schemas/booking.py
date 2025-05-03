from pydantic import BaseModel
from typing import Optional
from datetime import date

# Base schema to include common fields
class BookingBase(BaseModel):
    user_id: Optional[int]
    destination: Optional[str]
    departure_date: Optional[str]
    flight: Optional[bool]
    airline: Optional[str]
    hotel: Optional[bool]
    hotel_name: Optional[str]
    total_cost: Optional[float]
    associated_trip_id: Optional[int]

# Schema for creating a booking (includes user_id)
class BookingCreate(BaseModel):
    user_id: Optional[int]
    flight: Optional[bool]
    airline: Optional[str]
    hotel: Optional[bool]
    hotel_name: Optional[str]
    associated_trip_id: Optional[int]


# Schema for updating a user (optional fields)
class BookingUpdate(BaseModel):
    flight: Optional[bool]
    airline: Optional[str]
    hotel: Optional[bool]
    hotel_name: Optional[str]

# Schema that includes the response model for user
class Booking(BookingBase):
    booking_id: Optional[int]

    class Config:
        orm_mode = True
