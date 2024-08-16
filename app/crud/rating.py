from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app import schemas, models, oauth2


def rate_movie(rate_payload: schemas.RatingCreate, movie_title: str, db: Session = Depends(), current_user: schemas.User = Depends(oauth2.get_current_user)):
    movie_in = db.query(models.Movie).filter(
        models.Movie.title == movie_title).first()
    if not movie_in:
        raise HTTPException(
            status_code=404,
            detail=f"{movie_title}' not found"
        )

    new_rate = models.Rating(**rate_payload.model_dump(),
                             movie_id=movie_in.id, user_id=current_user.id)
    db.add(new_rate)
    db.commit()
    db.refresh(new_rate)
    return new_rate


def get_ratings_by_movie(movie_title: str, db: Session = Depends()):
    movie_in = db.query(models.Movie).filter(
        models.Movie.title == movie_title).first()
    if not movie_in:
        return False
    return db.query(models.Rating).filter(models.Rating.movie_id == movie_in.id).all()


def confirm_rating(movie_title: str, db: Session = Depends(), current_user: schemas.User = Depends(oauth2.get_current_user)):
    movie = db.query(models.Movie).filter(
        models.Movie.title == movie_title).first()
    return db.query(models.Rating).filter(models.Rating.movie_id == movie.id, models.Rating.user_id == current_user.id).first()
