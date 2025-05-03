from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import booking as model
from ..models import user_trip_link
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_item = model.Booking(
        user_id=request["user_id"],
        destination=request["destination"],
        departure_date=request["departure_date"],
        flight=request["flight"],
        airline=request["airline"],
        hotel=request["hotel"],
        hotel_name=request["hotel_name"],
        total_cost=request["total_cost"],
        associated_trip_id=request["associated_trip_id"]
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Booking).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, booking_id):
    try:
        item = db.query(model.Booking).filter(model.Booking.booking_id == booking_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, booking_id, request):
    try:
        booking = db.query(model.Booking).filter(model.Booking.booking_id == booking_id)
        if not booking.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        booking.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return booking.first()


def delete(db: Session, booking_id):
    try:
        user = db.query(model.Booking).filter(model.Booking.booking_id == booking_id)
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        user.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)