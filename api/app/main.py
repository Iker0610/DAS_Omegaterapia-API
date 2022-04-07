import bcrypt
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from . import crud, api_models
from .database import SessionLocal

description: str = """
This api allows you to authorize as an Omegaterapia employee and retrieve user data.

==An internal auth-token is required for al entry-points.==


## Entry Points

### Authorization
With these entry points you can **authorize users** and **sign in** new users.

---

### Users
With these entry points you can **retrieve user data**.

---

### Messaging
With these entry points you can **send messages via FCM** to Omegaterapia employees.
"""

app = FastAPI(
    title="Omegaterapia API",
    description=description,
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


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
def create_user(user: api_models.UserAuth, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=user)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered.")
    return db_user


@app.get("/users/", response_model=list[api_models.User], status_code=status.HTTP_200_OK)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)


@app.post("/auth", response_model=api_models.User, status_code=status.HTTP_200_OK)
def authenticate_user(user_data: api_models.UserAuth, db: Session = Depends(get_db)):
    hashed_password = crud.get_user_password(db, username=user_data.username)
    if hashed_password is None or not bcrypt.checkpw(user_data.password.encode('utf-8'), hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect authorization information.")
    return user_data
