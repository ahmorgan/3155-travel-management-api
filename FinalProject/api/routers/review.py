from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..dependencies.database import get_db  # Import the database dependency
from ..controllers import review as controller  # Import the review controller
from ..schemas import review as schema  # Import the review schema

router = APIRouter(
    tags=['Reviews'],
    prefix="/reviews"
)

# Route to create a new review
@router.post("/", response_model=schema.Review, status_code=status.HTTP_201_CREATED)
def create_review(request: schema.ReviewCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

# Route to read all reviews
@router.get("/", response_model=list[schema.Review])
def read_all_reviews(db: Session = Depends(get_db)):
    return controller.read_all(db=db)

# Route to read a specific review by ID
@router.get("/{review_id}", response_model=schema.Review)
def read_review(review_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, review_id=review_id)

# Route to update a review
@router.put("/{review_id}", response_model=schema.Review)
def update_review(review_id: int, request: schema.ReviewUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, review_id=review_id)

# Route to delete a review by ID
@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, review_id=review_id)