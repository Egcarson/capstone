from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.crud import user as user_crud
import app.schemas as schemas
import app.database as database
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    tags=["User - Administration"]
)

# THIS USER END POINTS IS FOR DEVELOPMENT PURPOSES ONLY INCASE I FORGET TO REMOVE IT
# I know this endpoints was not included but just to efficiently handle users like viewing, deleting and updating added users..............................................................


@router.get('/users', status_code=status.HTTP_200_OK, response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    user = user_crud.get_users(skip, limit, db)
    return user


@router.get('/users/username/{username}', status_code=status.HTTP_200_OK, response_model=schemas.User)
def get_user_by_username(username: str, db: Session = Depends(database.get_db)):
    user = user_crud.get_user_by_username(username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get('/users/{id}', status_code=status.HTTP_200_OK, response_model=schemas.User)
def get_user_by_id(id: int, db: Session = Depends(database.get_db)):
    user = user_crud.get_user_by_id(id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put('/users/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.User)
def update_user(id: int, user_in: schemas.UserUpdate, db: Session = Depends(database.get_db)):

    logger.info("Updating User:")
    user = user_crud.get_user_by_id(id, db)
    if not user:
        logger.error(
            "An error occurred while updating. User not found. Updating aborted.........")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    update_user = user_crud.update_user(id, user_in, db)
    logger.info("User updated successfully")
    return update_user


@router.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(database.get_db)):

    logger.info('Deleting user:')
    user = user_crud.get_user_by_id(id, db)
    if not user:
        logger.error("An error has occurred while deleting")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    logger.info("User deleted successfully")
    return user_crud.delete_user(id, db)
