from sqlalchemy import Column, Integer, String, DECIMAL
from ..dependencies.database import Base


class Trip(Base):
    __tablename__ = "tourism_table"

    trip_id = Column(Integer, primary_key=True)
    location = Column(String(200))
    country = Column(String(200))
    category = Column(String(200))
    visitors = Column(Integer)
    rating = Column(DECIMAL)
    revenue = Column(DECIMAL)
    accomodation_available = Column(String(10))
    estimated_cost = Column(Integer)
    mode_of_travel = Column(String(50))
    start_date = Column(String(50))
    end_date = Column(String(50))



