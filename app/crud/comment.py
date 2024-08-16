from sqlalchemy.orm import Session, joinedload
from fastapi import Depends
from app import schemas, models, oauth2

'''
Add a comment to a movie (authenticated access)
View comments for a movie (public access)
Add comment to a comment i.e nested comments (authenticated access)
'''


def add_comment(comment_payload: schemas.CommentCreate, movie_title: str, db: Session = Depends(), current_user: schemas.User = Depends(oauth2.get_current_user)):
    movie = db.query(models.Movie).filter(
        models.Movie.title == movie_title).first()
    if not movie:
        return False

    comment = models.Comment(
        **comment_payload.model_dump(), user_id=current_user.id, movie_id=movie.id, parent_id=None)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comments_for_movie(movie_title: str, skip: int = 0, limit: int = 10, db: Session = Depends()):
    movie = db.query(models.Movie).filter(
        models.Movie.title == movie_title).first()
    if not movie:
        return False
    movie_data = db.query(models.Comment).filter(
        models.Comment.movie_id == movie.id).offset(skip).limit(limit).all()
    return movie_data


def get_comment_by_id(comment_id: int, db: Session = Depends()):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def add_nested_comment(reply: schemas.CommentCreate, parent_id: int, current_user: int, db: Session = Depends()):
    parent_comment = db.query(models.Comment).filter(
        models.Comment.id == parent_id).first()

    reply_count = db.query(models.Comment).filter(
        models.Comment.parent_id == parent_comment.id).count()

    if not parent_comment:
        return False
    comment = models.Comment(
        comment_text=reply.comment_text, user_id=current_user.id, movie_id=parent_comment.movie_id, parent_id=parent_comment.id)

    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comment_with_replies(comment_id: int, db: Session = Depends()):
    comment = db.query(models.Comment).options(joinedload(
        models.Comment.replies)).filter(models.Comment.id == comment_id).all()
    if not comment:
        return None
    return comment

    # def to_dict(comment):
    #     return {
    #         "id": comment.id,
    #         "comment_text": comment.comment_text,
    #         "created_at": comment.created_at,
    #         "user_id": comment.user_id,
    #         "movie_id": comment.movie_id,
    #         "user": {
    #             "username": comment.user.username
    #         }if comment.user.username else None,
    #         "replies": [to_dict(reply) for reply in (comment.replies or [])]
    #     }
    # return to_dict(comment)
