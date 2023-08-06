from fastapi import FastAPI,Response, status, HTTPException, Depends

from typing import List
from . import model,schema,utils
from sqlalchemy.orm import Session
from .database import engine
from .Router import posts,users

model.Base.metadata.create_all(bind=engine)
#postgres database
app = FastAPI()

app.include_router(posts.router)

app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Hello World"}