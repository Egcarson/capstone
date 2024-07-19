from fastapi import APIRouter, status, HTTPException, Depends  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import crud.user
import schemas
import database
import crud
import utils

router = APIRouter(
    tags=["Authentication"]
)


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def signup(user_in: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user_check = crud.user.get_user_by_username(
        username=user_in.username, db=db)
    email_check = crud.user.get_user_by_email(email=user_in.email, db=db)

    if user_check or email_check:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User already exists!"
        )
    hashed_password = utils.hash_password(password=user_in.password)
    user_in.password = hashed_password
    new_user = crud.user.create_users(user_in=user_in, db=db)
    return new_user


@router.post("/login")
def login(current_user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = crud.user.get_user_by_username(current_user.username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    rehashed_password = utils.verify_hashed_password(
        current_user.password, user.password)
    if not rehashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    # create access token

    # return access token
    return {"message": "Access token"}
