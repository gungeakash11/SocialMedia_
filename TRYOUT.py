from fastapi import FastAPI, Response, status, HTTPException
from random import randrange
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = [
    {"name": "foo", "age": 30},
    {"name": "bar", "age": 28},
]

class User(BaseModel):
    name: str
    age: int

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    users.append(user.dict())
    return user

@app.get("/users", response_model=List[User])
def get_users():
    return users