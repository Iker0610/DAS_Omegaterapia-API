from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from . import crud, api_models
from .database import SessionLocal

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------
# Entry-Points
# ---------------------------------------------------------


@app.get("/")
async def root():
    return RedirectResponse(url='/docs')


@app.post("/users/", response_model=api_models.UserBase, status_code=status.HTTP_201_CREATED)
def create_user(user: api_models.UserAuth, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered.")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[api_models.UserBase], status_code=status.HTTP_200_OK)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)


@app.post("/auth", response_model=api_models.UserBase, status_code=status.HTTP_200_OK)
def authenticate_user(user_data: api_models.UserAuth, db: Session = Depends(get_db)):
    user_password = crud.get_user_password(db, username=user_data.username)
    if user_password is None or user_password != user_data.hashed_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect authorization information.")
    return user_data.username
