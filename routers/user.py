from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
import database
import crud.user
import schemas
import database
import crud
import utils

router = APIRouter(
    tags=["User"]
)


@router.get('/users', response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    user = crud.user.get_users(skip, limit, db)
    return user


@router.get('/users/username/{username}', response_model=schemas.User)
def get_user_by_username(username: str, db: Session = Depends(database.get_db)):
    user = crud.user.get_user_by_username(username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get('/users/{id}', response_model=schemas.User)
def get_user_by_id(id: int, db: Session = Depends(database.get_db)):
    user = crud.user.get_user_by_id(id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put('/users/{id}', response_model=schemas.User)
def update_user(id: int, user_in: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    user = crud.user.get_user_by_id(id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    update_user = crud.user.update_user(id, user_in, db)
    return update_user
