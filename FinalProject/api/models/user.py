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
