from sqlalchemy.orm import Session

from . import entities, api_models


def get_user(db: Session, username: str) -> entities.User | None:
    return db.query(entities.User).filter(entities.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[str]:
    return db.query(entities.User.username).offset(skip).limit(limit).all()


def get_user_password(db: Session, username: str) -> bytes | None:
    return db.query(entities.User.hashed_password).filter(entities.User.username == username).first()


def create_user(db: Session, user: api_models.UserAuth) -> entities.User | None:
    if get_user(db, username=user.username):
        return None
    else:
        db_user = entities.User(username=user.username, hashed_password=user.hashed_password())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
