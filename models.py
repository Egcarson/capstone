from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from database import Base

# User details


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)

    movies = relationship("Movie", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    ratings = relationship("Rating", back_populates="user")


class Movie(Base):

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(TIMESTAMP(timezone=True),
                          server_default=text('now()'), nullable=False)
    genre = Column(String, nullable=False)
    director = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="movies")
    comments = relationship("Comment", back_populates="movie")
    ratings = relationship("Rating", back_populates="movie")


class Comment(Base):

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    comment_text = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    movie_id = Column(Integer, ForeignKey(
        "movies.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="comments")
    movie = relationship("Movie", back_populates="comments")


class Rating(Base):

    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    movie_id = Column(Integer, ForeignKey(
        "movies.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")
