from typing import Optional

from pydantic import BaseModel,ConfigDict, EmailStr, conint
from datetime import datetime


#User
# Request
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Response
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # to display our ORM response
    model_config = ConfigDict(from_attributes=True)


# Post
# Request
class PostBase(BaseModel):
    title: str
    content : str
    published: bool = True


class PostCreate(PostBase):
    pass

# Response
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # to display our ORM response
    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    Post: Post
    votes: int

    # to display our ORM response
    model_config = ConfigDict(from_attributes=True)




#update Password
# class updateUserPassword(UserCreate):
#     new_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


#token schema

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None


# vote

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)