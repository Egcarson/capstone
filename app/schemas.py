from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional, List, Union

# users


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    username: str

    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime = datetime.now()

    model_config = ConfigDict(from_attributes=True)


class Rating(BaseModel):
    id: int
    rating: float
    user_id: int
    movie_id: int

    model_config = ConfigDict(from_attributes=True)


class RatingOut(BaseModel):
    user: Optional[UserOut]
    rating: float

    model_config = ConfigDict(from_attributes=True)


class RatingOut2(BaseModel):
    id: int
    rating: float
    user: Optional[UserOut]

    model_config = ConfigDict(from_attributes=True)


class RatingResponse(BaseModel):
    message: str
    data: List[RatingOut2]


class CommentBase(BaseModel):
    comment_text: str


class CommentCreate(CommentBase):
    pass


class CommentOut(BaseModel):
    user: Optional[UserOut]
    id: int
    comment_text: str
    created_at: datetime = datetime.now()

    model_config = ConfigDict(from_attributes=True)


class CommentReplyOut(BaseModel):
    user: Optional[UserOut]
    id: int
    # assigning a parent id to the response to tell a comment from a reply
    parent_id: Optional[int] = None
    comment_text: str
    created_at: datetime = datetime.now()

    model_config = ConfigDict(from_attributes=True)


class CommentResponse(BaseModel):
    message: str
    data: CommentOut

    model_config = ConfigDict(from_attributes=True)


class Comment(CommentBase):
    id: int
    created_at: datetime = datetime.now()
    user_id: int
    movie_id: int

    model_config = ConfigDict(from_attributes=True)

# movie


class MovieBase(BaseModel):
    title: str
    release_date: datetime = datetime.now()
    genre: str
    network: Optional[str] = "Netflix"
    director: List[str] = []


class MovieTitle(BaseModel):
    title: str

# this is here because it has to inherit movie title from MovieBase


class RatingOut(BaseModel):
    movie: Optional[MovieTitle]
    user: Optional[UserOut]
    rating: float

    model_config = ConfigDict(from_attributes=True)


class MovieRatingResponse(BaseModel):
    user: Optional[UserOut]
    rating: float

    model_config = ConfigDict(from_attributes=True)


class RatingOut2(BaseModel):
    id: int
    rating: float
    user: Optional[UserOut]

    model_config = ConfigDict(from_attributes=True)


class MovieCreate(MovieBase):
    pass


class MovieUpdate(MovieBase):
    pass


class Movie(MovieBase):
    id: int
    user_id: int
    user: Optional[UserOut]
    comments: List[CommentOut]
    ratings: Union[str, List[MovieRatingResponse]] = "No ratings available yet"

    model_config = ConfigDict(from_attributes=True)


# Comment response after creation


class MovieCommentResponse(BaseModel):
    title: str
    user: Optional[UserOut]
    comments: List[CommentOut]
    ratings: Union[str, List[RatingOut]] = "No ratings available yet"

    model_config = ConfigDict(from_attributes=True)


class MovieRatingResponse(BaseModel):
    title: str
    user: Optional[UserOut]
    comments: List[CommentOut]
    ratings: Union[str, List[RatingOut]] = "No ratings available yet"

    model_config = ConfigDict(from_attributes=True)


class MovieResponse(BaseModel):
    message: str
    data: List[Movie]

# comment


# rating


class RatingCreate(BaseModel):
    rating: float  # Field(..., ge=0, le=5,
    # description="Rating is between 0 and 5.0")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
