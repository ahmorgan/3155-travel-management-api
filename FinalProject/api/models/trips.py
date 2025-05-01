from sqlalchemy import Column, Integer, String, VARCHAR, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Trip(Base):
    __tablename__ = "tourism_table"

    trip_id = Column(Integer, primary_key=True)
    location = Column(VARCHAR(200))
    country = Column(VARCHAR(200))
    category = Column(VARCHAR(200))
    visitors = Column(Integer)
    rating = Column(DECIMAL)
    revenue = Column(DECIMAL)
    accomodation_available = Column(VARCHAR(10))
    estimated_cost = Column(Integer)
    mode_of_travel = Column(VARCHAR(50))
    start_date = Column(VARCHAR(50))
    end_date = Column(VARCHAR(50))
    
    # Relationship to connect with UserTripLink table
    user_links = relationship("UserTripLink", back_populates="trip")

    # Code reference: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
    # This code converts SQLAlchemy objects to dictionaries, which makes them easily readable in the recommendation endpoint.
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
