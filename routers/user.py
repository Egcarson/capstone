from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
import crud.user
import schemas
import database
import crud
import utils

router = APIRouter(
    prefix='/users'
    tags=["User"]
)

@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user_check = crud.user.get_user_by_username(username=user_in.username, db=db)
    email_check = crud.user.get_user_by_email(email=user_in.email, db=db)

    if user_check or email_check:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User already exists!"
        )
    hashed_password = utils.hash_password(password=user_in.password)
    new_user = crud.user.create_users(**user_in.dict(), db=db)