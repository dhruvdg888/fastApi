
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
import psycopg2
from psycopg2.extras import RealDictCursor
from .. database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)
# Create User
@router.post("/", response_model=schemas.UserOut ,status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate ,db:Session = Depends(get_db)):

    #hashing the password
    
    user.password = utils.hash_password(user.password)

    new_user = models.User(**user.model_dump())
    email = user.model_dump()['email']
    
    existing_user = db.query(models.User).filter(models.User.email == email).first()

    if existing_user == None:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email id : {email} already exists")

    return new_user

# Get user by id
@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id: int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    
    return user

# Reset Password
# @router.put("/{id}",response_model=schemas.UserOut)
# def update_password(id:int ,user_data: schemas.updateUserPassword, db:Session = Depends(get_db)):
#     db_user = db.query(models.User).filter(models.User.id == id,models.User.email == user_data.email).first()

#     if not db_user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     if not utils.verify_password(user_data.password,db_user.password):
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    
#     db_user.password = utils.hash_password(user_data.new_password)

#     db.commit()
#     db.refresh(db_user)

#     return db_user