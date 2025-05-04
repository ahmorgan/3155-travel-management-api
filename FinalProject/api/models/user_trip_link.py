from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class UserTripLink(Base):
    __tablename__ = 'user_trip_link'
    # Link ID
    link_id = Column(Integer, primary_key=True)
    # User information related to booked trip
    user_id = Column(Integer, ForeignKey('users.user_id'))
    # Trip ID
    trip_id = Column(Integer, ForeignKey('tourism_table.trip_id'))
    # Date trip was booked
    date_booked = Column(DateTime, default=datetime.utcnow)
    # Relationship to connect with user and trip tables
    user = relationship("User", back_populates="trip_links")
    trip = relationship("Trip", back_populates="user_links")

    # Code reference: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
    # This code converts SQLAlchemy objects to dictionaries, which makes them easily readable in the recommendation endpoint.
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}