from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from random import randrange


class post(BaseModel):
    title: str
    content: str
    published: bool = True
