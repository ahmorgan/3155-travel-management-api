from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import review as model  # Import the review model
from ..schemas import review as schema  # Import the review schema
from ..models import user_trip_link as link_model # Import UserTripLink model
from sqlalchemy.exc import SQLAlchemyError


# Function to create a new review
def create(db: Session, request: schema.ReviewCreate):
    user_trip_link = db.query(link_model.UserTripLink).filter(
        link_model.UserTripLink.user_id == request.user_id,
        link_model.UserTripLink.trip_id == request.trip_id
    ).first()

    if not user_trip_link:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You haven't been on this trip!"
        )

    new_review = model.Review(
        user_id=request.user_id,
        trip_id=request.trip_id,
        rating=request.rating,
        comment=request.comment
    )
    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_review


# Function to read all reviews
def read_all(db: Session):
    try:
        reviews = db.query(model.Review).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return reviews


# Function to read a specific review by ID
def read_one(db: Session, review_id: int):
    try:
        review = db.query(model.Review).filter(model.Review.review_id == review_id).first()
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return review


# Function to update an existing review
def update(db: Session, review_id: int, request: schema.ReviewUpdate):
    try:
        review_query = db.query(model.Review).filter(model.Review.review_id == review_id)
        existing_review = review_query.first()

        if not existing_review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

        update_data = request.dict(exclude_unset=True)  # Get only the fields that were set
        review_query.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(review_query.first())
        return review_query.first()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)



# Function to delete a review by ID
def delete(db: Session, review_id: int):
    try:
        review_query = db.query(model.Review).filter(model.Review.review_id == review_id)
        if not review_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        review_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)