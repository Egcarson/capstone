from sqlalchemy.orm import Session
from fastapi import Depends
from app import schemas, models, oauth2

'''
Movie Listing:
View a movie added (public access)
Add a movie (authenticated access)
View all movies (public access)
Edit a movie (only by the user who listed it)
Delete a movie (only by the user who listed it)
'''


def create_movie(movie_in: schemas.MovieCreate, db: Session = Depends(), current_user: schemas.User = Depends(oauth2.get_current_user)) -> models.Movie:
    new_movie = models.Movie(**movie_in.model_dump(), user_id=current_user.id)
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie


def get_movies(skip: int = 0, limit: int = 10, db: Session = Depends()) -> models.Movie:
    return db.query(models.Movie).offset(skip).limit(limit).all()


def get_movie_by_id(id: int, db: Session = Depends()) -> models.Movie:
    return db.query(models.Movie).filter(models.Movie.id == id).first()


def get_movie_by_title(title: str, db: Session = Depends()) -> models.Movie:
    return db.query(models.Movie).filter(models.Movie.title == title).first()


def movie_validation(title: str, user_id: int, db: Session = Depends()) -> models.Movie:
    return db.query(models.Movie).filter(models.Movie.title == title, models.Movie.user_id == user_id).first()


def update_movie(title: str, movie_in: schemas.MovieUpdate, db: Session = Depends()) -> models.Movie:
    movie = get_movie_by_title(title, db)
    if not movie:
        return None

    movie_dict = movie_in.model_dump(exclude_unset=True)

    for k, v in movie_dict.items():
        setattr(movie, k, v)
    db.commit()
    db.refresh(movie)
    return movie


def delete_movie(title: str, db: Session = Depends()):
    movie = get_movie_by_title(title, db)
    if not movie:
        return None
    db.delete(movie)
    db.commit()

    return movie
