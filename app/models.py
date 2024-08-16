from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from app.database import Base

# User details


class User(Base):

    __tablename__ = "users"

    # add autoincrement constraint
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('CURRENT_TIMESTAMP'), nullable=False)

    movies = relationship("Movie", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    ratings = relationship("Rating", back_populates="user")


class Movie(Base):

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    release_date = Column(TIMESTAMP(timezone=True),
                          server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    genre = Column(String, nullable=False)
    network = Column(String, default="Netflix")
    director = Column(JSON, nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="movies")
    comments = relationship("Comment", back_populates="movie")
    ratings = relationship("Rating", back_populates="movie")


class Comment(Base):

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    comment_text = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    movie_id = Column(Integer, ForeignKey(
        "movies.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)

    user = relationship("User", back_populates="comments")
    movie = relationship("Movie", back_populates="comments")
    replies = relationship("Comment", backref='parent',
                           remote_side=[id], lazy='joined')


class Rating(Base):

    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    movie_id = Column(Integer, ForeignKey(
        "movies.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")
