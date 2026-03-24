from pydantic import BaseModel,ConfigDict
from datetime import datetime

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