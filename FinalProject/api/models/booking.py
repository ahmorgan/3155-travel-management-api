from sqlalchemy import Column, Integer, String, VARCHAR, DECIMAL, ForeignKey, BOOLEAN
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    destination = Column(VARCHAR(200))
    departure_date = Column(VARCHAR(200))
    flight = Column(BOOLEAN)
    airline = Column(VARCHAR(200))
    hotel = Column(BOOLEAN)
    hotel_name = Column(VARCHAR(200))
    total_cost = Column(DECIMAL)
    associated_trip_id = Column(Integer)


    # Code reference: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
    # This code converts SQLAlchemy objects to dictionaries, which makes them easily readable in the recommendation endpoint.
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}