# app/schemas.py this file defines the Pydantic models (schemas) for data validation and serialization.

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# Base schema containing common post fields (title, content, published status)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    


# Schema for creating a new post request
class PostCreate(PostBase):
    pass

# Schema for returning user information in responses (excludes password)
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    model_config = {"from_attributes": True}

# Schema for user login request (email & password)
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    model_config = {"from_attributes": True}

# Complete post schema including post details and owner information
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # Pydantic v2: 'orm_mode' was renamed to 'from_attributes'
    # Use `model_config` with `from_attributes` instead of Config.orm_mode
    # model_config = {"from_attributes": True}  # This allows Pydantic to read data from SQLAlchemy models
    model_config = {"from_attributes": True}

# Schema for post response with vote count aggregation
class PostOut(BaseModel):
    Post: Post
    votes: int
    model_config = {"from_attributes": True}


# Schema for user registration request (email & password)
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    model_config = {"from_attributes": True}


# Schema for vote request (post_id & direction: 1=upvote, 0=remove)
class Vote(BaseModel):
    post_id: int
    dir: int = Field(le=1) 
    # vote_id: int


# Schema for OAuth2 token response containing JWT and token type
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for JWT token payload containing user ID
class TokenData(BaseModel):
    id: Optional[int]  = None
