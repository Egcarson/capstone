from fastapi import APIRouter, status, HTTPException, Depends, Query  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from typing import List
from app.crud import comment as comment_crud, movies as movie_crud
from app import schemas, database, oauth2
from app.logger import get_logger

logger = get_logger(__name__)


router = APIRouter(
    tags=["Comment"]
)


@router.post('/comments', status_code=status.HTTP_201_CREATED, response_model=schemas.CommentResponse)
async def add_comment(comment_payload: schemas.CommentCreate, movie_title: str = Query(..., description="Insert the movie title"), db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    logger.info("Commenting on movie:")

    if not movie_title:
        logger.error("movie title not specified")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie title not specified"
        )
    # ----------------a user can add more than one comment to a movie
    comment = comment_crud.add_comment(
        comment_payload, movie_title, db, current_user)
    if not comment:
        logger.error("movie does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )

    logger.info("Successfully added comment for movie")
    return {"message": "successfully added", "data": comment}


@router.get('/comments/{movie_title}', status_code=status.HTTP_200_OK, response_model=List[schemas.CommentReplyOut])
async def get_comments(movie_title: str, skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):

    logger.info("Getting Comments:")
    if not movie_title:
        logger.error(
            "movie title not specified on action to get movie comments")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie title not specified"
        )

    movie = movie_crud.get_movie_by_title(movie_title, db)
    if not movie:
        logger.error("Movie not found on action to get movie comments")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )

    comments = comment_crud.get_comments_for_movie(
        movie_title, skip, limit, db)

    logger.info("Successfully fetched comments for movie")
    return comments


@router.post('/comments/{comment_id}/reply', status_code=status.HTTP_201_CREATED, response_model=schemas.CommentReplyOut)
async def add_nested_comment(reply: schemas.CommentCreate, comment_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    logger.info("Comment Reply Cretion:")
    if not comment_id:
        logger.warning("Parent ID not specified for nested comments")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please specify a comment id"
        )

    comment = comment_crud.get_comment_by_id(comment_id, db)
    if not comment:
        logger.warning("No comment with the specified id")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No comment with the id"
        )

    comment_reply = comment_crud.add_nested_comment(
        reply=reply, parent_id=comment_id, current_user=current_user, db=db)
    if not comment_reply:
        logger.error("Failed to add a reply to comment with the specified id")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add a reply to comment with the id"
        )

    logger.info("Successfully added reply to comment")
    return comment_reply

    # replies = comment_crud.get_comment_with_replies(comment_id, db)
    # return replie
