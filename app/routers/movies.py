from fastapi import APIRouter, status, HTTPException, Depends, Query  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from typing import List
import app.crud.user as user_crud
import app.crud.movies as movie_crud
from app import schemas, database, oauth2, models
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    tags=["Movie"]
)
'''
View a movie added (public access)
Add a movie (authenticated access)
View all movies (public access)
Edit a movie (only by the user who listed it)
Delete a movie (only by the user who listed it)
'''


@router.get('/movies', status_code=status.HTTP_200_OK, response_model=List[schemas.Movie])
async def get_movies(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):

    logger.info("Getting movies from database..........")
    movies = movie_crud.get_movies(skip, limit, db)

    logger.info("Movies were retrieved successfully")
    return movies


@router.post('/movies', status_code=status.HTTP_201_CREATED, response_model=schemas.Movie)
def create_movie(movie_in: schemas.MovieCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    logger.info("Movie creation:")
    # validating if the movie have already been created by the current user
    user = user_crud.get_user_by_id(id=current_user.id, db=db)

    validate_create_request = movie_crud.movie_validation(
        title=movie_in.title, user_id=user.id, db=db)

    if validate_create_request:
        logger.warning(
            "this user have already listed this movie, movie listing aborted....")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hello, you've already added this movie. Please check your list of movies."
        )

    new_movie = movie_crud.create_movie(movie_in, db, current_user)
    logger.info("Movie added successfully")
    return new_movie


@router.get('/movies/{title}', status_code=status.HTTP_200_OK, response_model=schemas.Movie)
def get_movie_title(title: str, db: Session = Depends(database.get_db)):

    logger.info("User about to get a movie by title:")

    movie = movie_crud.get_movie_by_title(title=title, db=db)
    if not movie:
        logger.warning(
            "An error occurred while retreiving the movie. Movie not found and aborted.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sorry dear, movie not exist. Please check back later."
        )
    logger.info(
        "Request completed. Movie is available and retrieved successfully.")
    return movie


@router.put('/movies/{title}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Movie)
def update_movie(title: str, movie_in: schemas.MovieUpdate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    logger.info("An attempt to update movie has been made:")
    movie = movie_crud.get_movie_by_title(title, db)
    if not movie:
        logger.error("movie not found. Movie update failed.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Oops!....we can't find this movie. Please try again"
        )

    logger.info("Validating if the user is authorized to update movie.")
    if int(movie.user_id) != int(current_user.id):
        logger.error("An error occurred while updating. User not authorized.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Failed. you are not allowed to perform the requested action."
        )

    logger.info("Update intitiated")
    update_movie = movie_crud.update_movie(title, movie_in, db)
    logger.info("Update on movie is successful.")
    return update_movie


@router.delete('/movies/{title}', status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(title: str, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    logger.info("Deleting a movie from database:")

    movie = movie_crud.get_movie_by_title(title, db)
    if not movie:
        logger.error("An error occured. Movie not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Oops!....we can't find the movie. Please try again"
        )

    logger.info("Validating if the user is authorized to delete a movie.")
    if int(movie.user_id) != int(current_user.id):
        logger.error("Validation failed. Request aborted..............")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Failed. you are not allowed to perform the requested action."
        )
    logger.info("Validation successful. Movie have been deleted successfully.")
    return movie_crud.delete_movie(title, db)
