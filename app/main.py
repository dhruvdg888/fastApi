from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post,user,auth, vote
from .config import settings

# we don't need this now as we are using alembic to update the database dynamically
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#list of domains that allow CORS
# origins = ["https://www.google.com", "https://www.youtube.com"]

# here for all the domains (global)
origins = ["*"]

#to allow CORS (Cross Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI application!"}






    
