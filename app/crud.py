
from jose import jwt

from typing import List
from datetime import timedelta, datetime
from passlib.context import CryptContext


from app.config import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


dummy_user = {
    "email": "chisanga@megacog.com",
    "hashed_password": pwd_context.hash("123456789") 
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(email: str, password: str):
    if email != dummy_user["email"]:
        return False
    
    if not verify_password(password, dummy_user["hashed_password"]):
        return False
    
    return {"email": dummy_user["email"]}

async def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
