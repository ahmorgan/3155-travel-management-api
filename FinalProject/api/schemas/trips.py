from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TripBase(BaseModel):
    location: str
    country: str
    category: str
    accomodation_available: str
    estimated_cost: int
    mode_of_travel: str
    start_date: str
    end_date: str


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    location: Optional[str]
    country: Optional[str]
    category: Optional[str]
    visitors: Optional[int]
    rating: Optional[float]
    revenue: Optional[float]
    accomodation_available: Optional[str]
    estimated_cost: Optional[int]
    mode_of_travel: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]


class Trip(TripBase):
    trip_id: int
    visitors: int
    rating: float
    revenue: float

    class ConfigDict:
        from_attributes = True