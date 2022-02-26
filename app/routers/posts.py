from fastapi import (APIRouter,
                    HTTPException,
                    status,
                    Depends)
from typing import List
from sqlalchemy.orm import Session
import models
import schemas
import oauth2
from database import get_db


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post("/create", status_code=status.HTTP_201_CREATED,
                response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/all", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    all_posts = db.query(models.Post).all()
    return all_posts


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post


@router.put("/update/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), 
                   current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


@router.delete("/delete/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    delete_post = db.query(models.Post).filter(models.Post.id == id)

    if not delete_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"delete post with id: {id} does not exist")

    delete_post.delete(synchronize_session=False)
    db.commit()

    return {"status": "successfully deleted"}
