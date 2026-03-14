# app/schemas.py this file defines the Pydantic models (schemas) for data validation and serialization.

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    """Base Pydantic schema for post data.
    
    Contains common post fields used as a base for post creation and responses.
    
    Attributes:
        title (str): The title of the post.
        content (str): The content/body of the post.
        published (bool): Whether the post is published (default: True).
    """
    title: str
    content: str
    published: bool = True
    


class PostCreate(PostBase):
    """Pydantic schema for creating a new post.
    
    Inherits all fields from PostBase and is used for validating
    incoming post creation requests.
    """
    pass

class UserOut(BaseModel):
    """Pydantic schema for user response data.
    
    Used in API responses to return user information while excluding
    sensitive data like passwords. Configured to read from SQLAlchemy ORM objects.
    
    Attributes:
        id (int): The unique user identifier.
        email (str): The user's email address.
        created_at (datetime): When the user account was created.
    """
    id: int
    email: EmailStr
    created_at: datetime
    model_config = {"from_attributes": True}

class UserLogin(BaseModel):
    """Pydantic schema for user login requests.
    
    Validates incoming login requests with email and password credentials.
    
    Attributes:
        email (str): The user's email address.
        password (str): The user's password for authentication.
    """
    email: EmailStr
    password: str
    model_config = {"from_attributes": True}

class Post(PostBase):
    """Complete Pydantic schema for a post with owner information.
    
    Extends PostBase with additional fields including post ID, creation timestamp,
    and the owner's user information. Configured to read from SQLAlchemy ORM objects.
    
    Attributes:
        id (int): The unique post identifier.
        created_at (datetime): When the post was created.
        owner_id (int): The ID of the user who owns the post.
        owner (UserOut): User object containing owner information (name and email).
    """
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    model_config = {"from_attributes": True}

class PostOut(BaseModel):
    """Pydantic schema for post response with vote count aggregation.
    
    Wraps a Post object with the total count of votes/upvotes for that post.
    Used in API responses when returning posts with vote statistics.
    
    Attributes:
        Post (Post): The post object containing all post details and owner info.
        votes (int): The total number of votes/upvotes on the post.
    """
    Post: Post
    votes: int
    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    """Pydantic schema for user registration requests.
    
    Validates incoming user registration requests with email and password.
    
    Attributes:
        email (str): The user's email address.
        password (str): The user's password (will be hashed before storage).
    """
    email: EmailStr
    password: str
    model_config = {"from_attributes": True}


class Vote(BaseModel):
    """Pydantic schema for vote requests.
    
    Validates incoming vote requests. Supports upvoting (dir=1) and removing votes (dir=0).
    
    Attributes:
        post_id (int): The ID of the post being voted on.
        dir (int): Vote direction: 1=upvote, 0=remove vote. Must be <= 1.
    """
    post_id: int
    dir: int = Field(le=1)


class Token(BaseModel):
    """Pydantic schema for OAuth2 token response.
    
    Returned after successful user authentication. Contains a JWT access token
    and the token type (typically 'bearer').
    
    Attributes:
        access_token (str): The JWT access token for authenticated requests.
        token_type (str): The token type (e.g., 'bearer').
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Pydantic schema for JWT token payload data.
    
    Contains the claims/payload information extracted from a JWT token.
    
    Attributes:
        id (Optional[int]): The user ID encoded in the token (can be None if not set).
    """
    id: Optional[int]  = None
