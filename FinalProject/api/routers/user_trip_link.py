from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from ..controllers import user_trip_link as controller
from ..schemas import user_trip_link as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["User-Trip Links"],
    prefix="/user-trip-links"
)

# POST route to create a new user-trip link
@router.post("/", response_model=schema.UserTripLink)
def create(request: schema.UserTripLinkCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

# GET route to read all user-trip links
@router.get("/", response_model=list[schema.UserTripLink])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

# GET route to read one user-trip link by ID
@router.get("/{link_id}", response_model=schema.UserTripLink)
def read_one(link_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, link_id=link_id)

# PUT route to update a user-trip link
@router.put("/{link_id}", response_model=schema.UserTripLink)
def update(link_id: int, request: schema.UserTripLinkUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, link_id=link_id, request=request)

# DELETE route to delete a user-trip link
@router.delete("/{link_id}")
def delete(link_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, link_id=link_id)
