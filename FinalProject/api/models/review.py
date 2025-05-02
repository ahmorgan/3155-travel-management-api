from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Review(Base):
    __tablename__ = "reviews_table"

    review_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))  # Foreign key to users table
    trip_id = Column(Integer, ForeignKey("tourism_table.trip_id"))  # Foreign key to trips table
    rating = Column(Integer)  # Rating on a scale (e.g., 1-5)
    comment = Column(String(500), nullable=True)  # Optional review text

    # Relationships to connect with User and Trip tables
    user = relationship("User", back_populates="reviews")
    trip = relationship("Trip", back_populates="reviews")
