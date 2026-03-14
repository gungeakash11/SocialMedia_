# app/models.py this file defines the database models using SQLAlchemy ORM.

from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Post(Base):
    """SQLAlchemy ORM model representing a post in the database.
    
    Attributes:
        id (int): Unique identifier for the post.
        title (str): Title of the post.
        content (str): Content/body of the post.
        published (bool): Flag indicating if the post is published (default: True).
        created_at (datetime): Timestamp of when the post was created (default: current time).
        owner_id (int): Foreign key referencing the user who owns the post.
        owner (User): Relationship to the User model representing the post owner.
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")

class User(Base):
    """SQLAlchemy ORM model representing a user in the database.
    
    Attributes:
        id (int): Unique identifier for the user.
        email (str): User's email address (must be unique).
        password (str): Hashed password for user authentication.
        created_at (datetime): Timestamp of when the user account was created (default: current time).
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column (String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Vote(Base):
    """SQLAlchemy ORM model representing a vote on a post.
    
    Represents a user's upvote on a post with a composite primary key.
    Uses CASCADE deletion to automatically remove votes when users or posts are deleted.
    
    Attributes:
        user_id (int): Foreign key referencing the user who cast the vote.
        post_id (int): Foreign key referencing the post being voted on.
    """
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
