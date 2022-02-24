from statistics import mode
from typing import Optional, List
from fastapi import (FastAPI,
                    status,
                    HTTPException,
                    Depends)
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import delete
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db

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


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.post("/create/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) returning * """, 
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title=post.title, 
    #                         content=post.content, 
    #                             published=post.published)

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" select * from posts """)
    # posts = cursor.fetchall()
    all_posts = db.query(models.Post).all()
    return all_posts


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""select * from posts where id = %s """, (str(id)))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} was not found")
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post


@app.put("/update/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning * """,
    #         (post.title, post.content, post.published, str(id)))
    # update_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


@app.delete("/delete/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""delete from posts where id = %s returning * """, (str(id)))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail=f"delete post with this id: {id} was not found")

    delete_post = db.query(models.Post).filter(models.Post.id == id)

    if not delete_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"delete post item with id: {id} was not found")
    
    delete_post.delete(synchronize_session=False)
    db.commit()

    return {"deleted_post": delete_post}
