from fastapi import FastAPI
"""
Root endpoint for the FastAPI application.
Returns:
    dict: A welcome message indicating the API is running.
"""
 #, Response, status, HTTPException, Depends
from . import models #, schemas, utils
from .database import engine #, get_db
from .routers import post, user, auth, vote
from .config import settings
#from random import randrange
# from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware



 
#models.Base.metadata.create_all(bind=engine) #-> we are using alembic for migrations so this line(Engine) is not needed anymore.

app = FastAPI()
"""Below Code is for CORS policy handling, allowing all origins to access the API. make changes in var 'origins' to restrict access."""
origins = ["*"]

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
    return {"messages": "Welcome to FastAPI! hahaha test"}


