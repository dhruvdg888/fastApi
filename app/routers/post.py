from typing import List

from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from fastapi.params import Body
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
from .. import models, schemas, oauth2
from .. database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# Get all the posts
@router.get("/", response_model= List[schemas.Post])
def get_posts(db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    #using SQL Alchemy ORM
    posts = db.query(models.Post).all()
    return posts

# Create post
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    new_post = models.Post(**post.model_dump(), owner_id=int(current_user.id))

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


# Get individual post
@router.get("/{id}",response_model=schemas.Post)
def get_post(id: int,db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post


# Delete a post
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):


    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} doesn't exist")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autherized to perform request action")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

    
# Update the post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate, db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    existing_post = post_query.first()


    if existing_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} doesn't exist")
    
    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autherized to perform request action")
    
    post_query.update(post.model_dump(),synchronize_session=False)

    db.commit()

    return post_query.first()
