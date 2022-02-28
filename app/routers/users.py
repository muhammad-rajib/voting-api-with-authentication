from fastapi import (APIRouter,
                    HTTPException,
                    status,
                    Depends)
from sqlalchemy.orm import Session
from app import models
from app import schemas
from app import utils
from app.database import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/create",
            status_code=status.HTTP_201_CREATED,
            response_model=schemas.CreateUserResponse)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    
    # hashing the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.CreateUserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"user with id: {id} does not exist")

    return user
