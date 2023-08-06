from fastapi import FastAPI,Response, status, HTTPException, Depends, APIRouter
from typing import List
from .. import model,schema,utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.UserOut)
def create_user(user:schema.UserCreate,db: Session = Depends(get_db)):
    #hash password
    user.password = utils.get_hashed_password(user.password)
    user = model.User(**user.dict())
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    return user 

@router.get("/{id}",response_model=schema.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user