from datetime import timedelta

from fastapi import APIRouter, HTTPException, status

from app.crud import authenticate_user, create_access_token, create_user
from app import schemas
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES


auth_router = APIRouter(prefix="/auth", tags=['Authentication'])



@auth_router.post("/login", response_model=schemas.Token)
async def login_for_access_token(user_login: schemas.UserLogin):
    user = await authenticate_user(user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user["email"]}, 
        expires_delta = access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")



@auth_router.post("/signup", response_model=schemas.User)
async def signup(user_create: schemas.UserCreate):
    try:
        new_user = await create_user(user_create)
        return new_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )