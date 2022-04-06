from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from . import crud, api_models
from .database import SessionLocal

# entities.Base.metadata.create_all(bind=engine)

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


@app.post("/users/", response_model=api_models.User, status_code=status.HTTP_201_CREATED)
def create_user(user: api_models.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_password(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered.")
    return crud.create_user(db=db, user=user)


@app.get("/users/{username}", response_model=api_models.User, status_code=status.HTTP_200_OK)
def read_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user
