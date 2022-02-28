from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import users, posts, auth, votes
from app.config import settings


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
