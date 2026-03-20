'''

C Create -> POST  /posts -> @app.post("/posts")

R Read -> GET /posts/:id or /posts ->  @app.get("/posts") or @app.get("/posts/{id}")

U Update -> PUT/PATCH  /posts/:id ->  @app.put("/posts/{id}")

D Delete -> DELETE  /posts/:id ->  @app.delete("/post/{id}")

'''


from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content : str
    published: bool = False
    rating: Optional[int] = None
    id: Optional[int] = None

#temp store
my_posts = [{"title":"title of post 1", "content":"content of post 1","id":1},{"title":"fav food", "content":"I like pizza","id":2}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None



@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI application!"}

# Get all the posts
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# Create post
@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,100000000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# Get individual post
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    return {"post_details": post}