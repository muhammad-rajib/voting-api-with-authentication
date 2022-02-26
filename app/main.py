from fastapi import FastAPI
import models
from database import engine
from routers import users, posts, auth
from config import settings

print(settings)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
