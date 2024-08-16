from fastapi import APIRouter, status, HTTPException, Depends  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from app.crud import rating as rating_crud, movies as movie_crud
from app.crud import user as user_crud
from app import schemas, oauth2, database
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    tags=["Rating"]
)


@router.post('/ratings', status_code=status.HTTP_201_CREATED, response_model=schemas.RatingOut)
async def rate_movie(rating_payload: schemas.RatingCreate, movie_title: str, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    logger.info("Rating:")
    movie = movie_crud.get_movie_by_title(movie_title, db)
    if not movie:
        logger.error("Movie not found. Rating aborted....................")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Movie not found. please check the typo or try again later"
        )

    # setting ratings to be between 0 and 5
    logger.info("Validating if the rating value is withing 0  and 5")
    if rating_payload.rating > 5:
        logger.error("Validation failed")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Please rating should be between 0 and 5.0"
        )

    # adding this section of code to accept rating only once
    user = user_crud.get_user_by_id(id=current_user.id, db=db)
    check_rating_status = rating_crud.confirm_rating(
        movie_title, db, current_user)
    if check_rating_status:
        logger.error(
            "This movie has already been rated by the current user. Rating aborted............")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Sorry dear, rating is only allowed once."
        )

    rated_movie = rating_crud.rate_movie(
        rating_payload, movie_title, db, current_user)

    logger.info("Rated successfully.")
    return rated_movie


@router.get('/ratings', status_code=status.HTTP_200_OK, response_model=list[schemas.RatingOut2])
def get_movie_rating(movie_title: str, db: Session = Depends(database.get_db)):

    logger.info("Request to get Ratings:")
    if not movie_title:
        logger.error(
            "An error ocurred. movie title not specicified. Request aborted.............")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing movie title"
        )
    ratings = rating_crud.get_ratings_by_movie(movie_title, db)

    movie_check = movie_crud.get_movie_by_title(movie_title, db)

    if not movie_check:
        logger.error(
            "An error ocurred. movie does not exist. Request aborted.............")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No movie found"
        )

    logger.info("Successfully retreieved ratings for specified movie.")
    return ratings
