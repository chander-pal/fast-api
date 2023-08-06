from fastapi import FastAPI,Response, status, HTTPException, Depends, APIRouter
from typing import List
from .. import model,schema
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/posts",tags=["Posts"])

@router.get("/",response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    my_posts = db.query(model.Post).all()
    return my_posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def create_posts(post:schema.PostCreate,db: Session = Depends(get_db)):
    post = model.Post(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/{id}",response_model=schema.Post)
def get_post(id: int,db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id)
    print(post.first())
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED,response_model=schema.Post)
def update_post(id: int, post: schema.PostCreate,db: Session = Depends(get_db)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post_update = post_query.first()
    if post_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()

