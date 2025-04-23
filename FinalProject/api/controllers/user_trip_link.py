from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import user_trip_link as model
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


def create(db: Session, request):
    new_link = model.UserTripLink(
        user_id=request.user_id,
        trip_id=request.trip_id,
        date_booked=request.date_booked if hasattr(request, "date_booked") else datetime.utcnow()
    )

    try:
        db.add(new_link)
        db.commit()
        db.refresh(new_link)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_link


def read_all(db: Session):
    try:
        return db.query(model.UserTripLink).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_one(db: Session, link_id: int):
    try:
        link = db.query(model.UserTripLink).filter(model.UserTripLink.link_id == link_id).first()
        if not link:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link ID not found!")
        return link
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def update(db: Session, link_id: int, request):
    try:
        link_query = db.query(model.UserTripLink).filter(model.UserTripLink.link_id == link_id)
        existing_link = link_query.first()
        if not existing_link:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link ID not found!")

        update_data = request.dict(exclude_unset=True)
        link_query.update(update_data, synchronize_session=False)
        db.commit()
        return link_query.first()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def delete(db: Session, link_id: int):
    try:
        link_query = db.query(model.UserTripLink).filter(model.UserTripLink.link_id == link_id)
        if not link_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link ID not found!")
        link_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
