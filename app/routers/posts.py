from fastapi import (APIRouter,
                    Response,
                    HTTPException,
                    status,
                    Depends)
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import (
    models,
    schemas,
    oauth2
)
from app.database import get_db


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post("/create", status_code=status.HTTP_201_CREATED,
                response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/all", response_model=List[schemas.PostVoteResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    """
    # Posts only for specific logged in user
    all_posts = db.query(models.Post).filter(
        models.Post.owner_id == current_user.id
    ).all()
    """
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).filter(
        models.Post.title.contains(search)
    ).limit(limit).offset(skip).all()

    return posts


@router.get("/{id}", response_model=schemas.PostVoteResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """ Return specific id post """
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")
    ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id
    ).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    """
    # Post only for specific logged in owner of this post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    """
    return post


@router.put("/update/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), 
                   current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


@router.delete("/delete/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    delete_post = db.query(models.Post).filter(models.Post.id == id)

    post = delete_post.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"delete post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    delete_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
