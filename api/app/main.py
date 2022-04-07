import bcrypt
from fastapi import Depends, FastAPI, HTTPException, status, UploadFile, File, Request
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session

from . import crud, api_models
from .database import SessionLocal

description: str = """
This api allows you to authorize as an Omegaterapia employee and retrieve user data.

*An internal auth-token is required for al entry-points.*


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
    version="1.0.0",
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

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url='/docs')


@app.post("/users/", tags=["Users"],
          response_model=api_models.User, status_code=status.HTTP_201_CREATED,
          responses={400: {"description": "Password is not valid."}, 409: {"description": "Username already registered."}}, )
async def create_user(user: api_models.UserAuth, db: Session = Depends(get_db)):
    if len(user.password) < 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is not valid.")

    if not (db_user := crud.create_user(db=db, user=user)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered.")
    return db_user


@app.get("/users/", response_model=list[api_models.User], status_code=status.HTTP_200_OK, tags=["Users"])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)


@app.post("/auth", tags=["Authentication"],
          response_model=api_models.User, status_code=status.HTTP_200_OK,
          responses={401: {"description": "Incorrect authorization information."}})
async def authenticate_user(user_data: api_models.UserAuth, db: Session = Depends(get_db)):
    hashed_password = crud.get_user_password(db, username=user_data.username)
    if hashed_password is None or not bcrypt.checkpw(user_data.password.encode('utf-8'), hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect authorization information.")
    return user_data


@app.get("/users/{username}/profile/image", response_class=FileResponse)
async def get_user_profile_image(username: str, db: Session = Depends(get_db)):
    if not (user_profile_image_url := crud.get_user_profile_image_url(db, username=username)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exists.")

    return user_profile_image_url


@app.post("/users/{username}/profile/image")
async def set_user_profile_image(username: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not (user := crud.get_user(db, username)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exists.")

    path = f'/omegaterapia_api/images/{username}'

    if crud.set_user_profile_image_url(db, user, path):
        contents = await file.read()
        with open(path, 'wb') as f:
            f.write(contents)
