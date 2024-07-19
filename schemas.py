from pydantic import BaseModel, EmailStr
from datetime import datetime

# users


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class UserLogin(BaseModel):
    username: str
    password: str


class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime = datetime.now()

    class Config:
        orm_mode = True

# movie


class MovieBase(BaseModel):
    title: str
    release_date: datetime = datetime.now()
    genre: str
    director: str


class MovieCreate(MovieBase):
    pass


class MovieUpdate(MovieBase):
    pass


class Movie(MovieBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# comment


class CommentBase(BaseModel):
    comment_text: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    created_at: datetime = datetime.now()
    user_id: int
    movie_id: int
