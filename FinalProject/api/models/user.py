from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True) # User ID
    username = Column(String(50)) # Username
    password = Column(String(50)) # Password
    # Relationship to connect with UserTripLink table
    trip_links = relationship("UserTripLink", back_populates="user")
    reviews = relationship("Review", back_populates="user")

    # Code reference: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
    # This code converts SQLAlchemy objects to dictionaries, which makes them easily readable in the recommendation endpoint.
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
