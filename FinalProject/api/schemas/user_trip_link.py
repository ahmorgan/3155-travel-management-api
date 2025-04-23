from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserTripLinkBase(BaseModel):
    user_id: int
    trip_id: int
    date_booked: Optional[datetime] = None

class UserTripLinkCreate(UserTripLinkBase):
    pass

class UserTripLinkUpdate(BaseModel):
    user_id: Optional[int]
    trip_id: Optional[int]
    date_booked: Optional[datetime]

class UserTripLink(UserTripLinkBase):
    link_id: int

    class Config:
        orm_mode = True
