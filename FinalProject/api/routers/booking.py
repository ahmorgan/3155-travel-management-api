from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import booking as controller
from ..schemas import booking as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Booking'],
    prefix="/booking"
)


@router.get("/", response_model=list[schema.Booking])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Booking)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, booking_id=item_id)


@router.put("/{item_id}", response_model=schema.Booking)
def update(item_id: int, request: schema.BookingUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, booking_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, booking_id=item_id)