from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models.trips import Trip
from ..schemas.trips import Trip as TripOut
from ..schemas.trip_planner import TripPlannerInput

router = APIRouter(
    prefix="/planner",
    tags=["Trip Planner"],
    responses={404: {"description": "No trips found"}}
)

@router.post("/recommend", response_model=list[TripOut])
def recommend_trips(
    input: TripPlannerInput,
    db: Session = Depends(get_db)
):
    """
    Get trips matching:
    - Country 
    - Within budget
    - Between dates (MM/DD/YYYY format)
    """
    query = db.query(Trip).filter(
        Trip.country.ilike(f"%{input.country}%"),
        Trip.estimated_cost <= input.budget,
        Trip.start_date >= input.start_date,  # Direct comparison
        Trip.end_date <= input.end_date       # No date conversion needed
    ).order_by(
        Trip.estimated_cost.asc(),
        Trip.rating.desc()
    )

    trips = query.all()
    if not trips:
        raise HTTPException(
            status_code=404,
            detail={"message": "No trips found", "criteria": input.dict()}
        )
    return trips
