# app/schemas.py this file defines the Pydantic models (schemas) for data validation and serialization.

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    


class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    phone_number: Optional[str] = None
    model_config = {"from_attributes": True}

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    model_config = {"from_attributes": True}

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # Pydantic v2: 'orm_mode' was renamed to 'from_attributes'
    # Use `model_config` with `from_attributes` instead of Config.orm_mode
    model_config = {"from_attributes": True}

class PostOut(BaseModel):
    Post: Post
    votes: int
    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    model_config = {"from_attributes": True}


class Vote(BaseModel):
    post_id: int
    dir: int = Field(le=1) 
    # vote_id: int


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]  = None
