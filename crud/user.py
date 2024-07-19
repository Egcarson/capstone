from sqlalchemy.orm import Session
from fastapi import Depends
import schemas
import database
import models


def create_users(user_in: schemas.UserCreate, db: Session = Depends()):
    new_user = models.User(**user_in.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(skip: int = 0, limit: int = 0, db: Session = Depends()):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_id(id: int, db: Session = Depends()):
    return db.query(models.User).filter(models.User.id == id).first()


def get_user_by_username(username: str, db: Session = Depends()):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(email: str, db: Session = Depends()):
    return db.query(models.User).filter(models.User.email == email).first()


def update_user(id: int, user_in: schemas.UserUpdate, db: Session = Depends()):
    user = get_user_by_id(id, db)
    if not user:
        return None

    user_dict = user_in.dict(exclude_unset=False)

    for k, v in user_dict.items():
        setattr(user, k, v)
    db.commit()
    return user


def delete_user(id: int, db: Session = Depends()):
    user = get_user_by_id(id, db)
    if not user:
        return None

    db.delete(user)
    db.commit()

    return user
