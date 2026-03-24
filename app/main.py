from typing import Optional, List

from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# while True:
#     try:
#         # here we will make these things working out simple rn, later we will make them more prod env friendly
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='#D1234G#', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was sucesfull!")
#         break
#     except Exception as error: 
#        print('Connecting to Database failed')
#        print('Error :', error)
#        time.sleep(2)



@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI application!"}


# Get all the posts
@app.get("/posts", response_model= List[schemas.Post])
def get_posts(db:Session = Depends(get_db)):

    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    

    #using SQL Alchemy ORM
    posts = db.query(models.Post).all()
    return posts

# Create post
@app.post("/posts",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db)):

    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))

    # new_post = cursor.fetchone()

    # to commit changes to data base
    # conn.commit()

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


# Get individual post
@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id: int,db:Session = Depends(get_db)):

    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post


# Delete a post
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db)):

    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} doesn't exist")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

    
# Update the post
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    existing_post = post_query.first()


    if existing_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} doesn't exist")
    
    post_query.update(post.model_dump(),synchronize_session=False)

    db.commit()

    return post_query.first()
