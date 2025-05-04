from pydantic import BaseModel, Field
from typing import Optional

# Base schema to include common fields
class ReviewBase(BaseModel):
    user_id: int = Field(..., description="ID of the user who wrote the review")
    trip_id: int = Field(..., description="ID of the trip being reviewed")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: Optional[str] = Field(None, max_length=500, description="Optional review comment")

# Schema for creating a review
class ReviewCreate(ReviewBase):
    pass

# Schema for updating a review
class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1 to 5")
    comment: Optional[str] = Field(None, max_length=500, description="Optional review comment")

# Schema for the review model
class Review(ReviewBase):
    review_id: int

    class Config:
        orm_mode = True