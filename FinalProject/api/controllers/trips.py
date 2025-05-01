from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import trips as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_item = model.Trip(
        trip_id=request["trip_id"],
        location=request["location"],
        country=request["country"],
        category=request["category"],
        accomodation_available=request["accomodation_available"],
        estimated_cost=request["estimated_cost"],
        mode_of_travel=request["mode_of_travel"],
        start_date=request["start_date"],
        end_date=request["end_date"]
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
        result = db.query(model.Trip).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_all_trip_categories(db: Session):
    try:
        result = set([elem[0] for elem in db.query(model.Trip.category).all()])
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return list(result)


def read_all_trip_locations(db: Session):
    try:
        result = set([elem[0] for elem in db.query(model.Trip.country).all()])
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return list(result)


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Trip).filter(model.Trip.trip_id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Trip).filter(model.Trip.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Trip).filter(model.Trip.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
