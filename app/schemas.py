from pydantic import BaseModel, EmailStr
from typing import Optional


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    First_name: str
    Last_name: str
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: EmailStr