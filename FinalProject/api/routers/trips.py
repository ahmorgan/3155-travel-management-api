from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import trips as controller
from ..schemas import trips as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Trips'],
    prefix="/trips"
)


@router.post("/", response_model=schema.Trip)
def create(request: schema.TripCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Trip])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Trip)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Trip)
def update(item_id: int, request: schema.TripUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
