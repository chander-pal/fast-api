from fastapi import FastAPI,Response, status, HTTPException, Depends

from typing import List
from . import model,schema,utils
from sqlalchemy.orm import Session
from .database import engine,get_db

model.Base.metadata.create_all(bind=engine)
#postgres database
app = FastAPI()




@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts",response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    my_posts = db.query(model.Post).all()
    return my_posts

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def create_posts(post:schema.PostCreate,db: Session = Depends(get_db)):
    post = model.Post(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.get("/posts/{id}",response_model=schema.Post)
def get_post(id: int,db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id)
    print(post.first())
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED,response_model=schema.Post)
def update_post(id: int, post: schema.PostCreate,db: Session = Depends(get_db)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post_update = post_query.first()
    if post_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()

@app.get("/random")
def random_number(db: Session = Depends(get_db)):
    posts = db.query(model.Post).all()
    return posts

@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schema.UserOut)
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
@app.get("/users/{id}",response_model=schema.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user