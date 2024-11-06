
from jose import jwt

from typing import List
from pydantic import EmailStr
from datetime import timedelta, datetime
from passlib.context import CryptContext
from app.schemas import UserCreate, User



from app.config import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


dummy_user = {
    "email": "chisanga@mage.com",
    "hashed_password": pwd_context.hash("123456789") 
}

users_db = []

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(email: EmailStr, password: str):
    user = next((u for u in users_db if u["email"] == email), None)
    
    if not user:
        return False
    
    if not verify_password(password, user["hashed_password"]):
        return False
    
    return {"email": user["email"]}

async def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_email(email: EmailStr):
    return next((user for user in users_db if user['email'] == email), None)

async def create_user(user: UserCreate):
    if get_user_by_email(user.email):
        raise ValueError("User already exists")
    
    hashed_password = pwd_context.hash(user.password)
    user_data = {"id": len(users_db) + 1,
                 "First Name": user.First_name,
                 "Last Name": user.Last_name,
                 "email": user.email,
                 "hashed_password": hashed_password
                }
    users_db.append(user_data)
    return User(id=user_data["id"], email=user_data["email"])