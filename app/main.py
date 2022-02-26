from turtle import pos
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import models
from database import engine
from routers import users, posts, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='fastapiuser',
            password='password123',
            cursor_factory=RealDictCursor 
        )
        cursor = conn.cursor()
        print('Database connection was succesfull!')
        break
    except Exception as error:
        print('Connecting to database failed')
        print('Error: ', error)


app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
