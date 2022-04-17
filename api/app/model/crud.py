from sqlalchemy.engine import row
from sqlalchemy.orm import Session

from . import entities
from .. import api_models


def get_user(db: Session, username: str) -> entities.User | None:
    return db.query(entities.User).filter(entities.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[row]:
    return db.query(entities.User.username).offset(skip).limit(limit).all()


def get_user_password(db: Session, username: str) -> bytes | None:
    result = db.query(entities.User.hashed_password).filter(entities.User.username == username).first()
    return result.hashed_password if result else result


def get_user_profile_image_url(db: Session, username: str) -> str | None:
    result = db.query(entities.User.profile_image_url).filter(entities.User.username == username).first()
    return result.profile_image_url if result else result


def set_user_profile_image_url(db: Session, user: str | entities.User, url: str) -> bool:
    if isinstance(user, str):
        user = get_user(db, user)

    if user:
        user.profile_image_url = url
        db.commit()
        db.refresh(user)

    return bool(user)


def create_user(db: Session, user: api_models.UserAuth) -> entities.User | None:
    if get_user(db, username=user.username):
        return None
    else:
        db_user = entities.User(username=user.username, hashed_password=user.hashed_password())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
