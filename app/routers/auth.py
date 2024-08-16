from fastapi import APIRouter, status, HTTPException, Depends  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import app.crud.user as user_crud
import app.schemas as schemas
from app import database, utils, oauth2, models
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    tags=["Authentication"]
)


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def signup(user_in: schemas.UserCreate, db: Session = Depends(database.get_db)):
    logger.info("Starting user creation...........")
    # validating if the user already exists
    user_check = user_crud.get_user_by_username(
        username=user_in.username, db=db)

    if user_check:
        logger.error("User already exists, aborting user creation...........")
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User already exists!"
        )

    hashed_password = utils.hash_password(password=user_in.password)
    user_in.password = hashed_password
    new_user = user_crud.create_users(user_in=user_in, db=db)
    logger.info("User created successfully...........")
    return new_user


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(current_user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    logger.info("User reqests loggin")
    user = user_crud.get_user_login(user_input=current_user.username, db=db)
    if not user:
        logger.error("User credentials not correct, aborting loggin")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    hashed_password = utils.verify_hashed_password(
        current_user.password, user.password)
    if not hashed_password:
        logger.error("User credentials not correct, aborting loggin")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    # create access token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    logger.info(f"access_token generated successfully. User with username: {
                current_user.username} logged in successfully")
    # return access token
    return {"access_token": access_token, "token_type": "Bearer"}
