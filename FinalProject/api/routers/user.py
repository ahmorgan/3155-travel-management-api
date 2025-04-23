from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..controllers import user as controller
from ..schemas import user as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Users'],
    prefix="/users"
)

# POST route to create a new user
@router.post("/", response_model=schema.User)
def create(request: schema.UserCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

# GET route to read all users
@router.get("/", response_model=list[schema.User])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

# GET route to read a specific user by ID
@router.get("/{user_id}", response_model=schema.User)
def read_one(user_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, user_id=user_id)

# PUT route to update a user's details
@router.put("/{user_id}", response_model=schema.User)
def update(user_id: int, request: schema.UserUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, user_id=user_id)

# DELETE route to delete a user by ID
@router.delete("/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, user_id=user_id)
