from fastapi import FastAPI
from starlette.responses import RedirectResponse
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

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


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
