from pydantic import BaseModel,ConfigDict, EmailStr
from datetime import datetime

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

    # to display our ORM response
    model_config = ConfigDict(from_attributes=True)



#User
# Request
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Response
class UserOut(BaseModel):
    id: int
    email: EmailStr


#update Password
# class updateUserPassword(UserCreate):
#     new_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str