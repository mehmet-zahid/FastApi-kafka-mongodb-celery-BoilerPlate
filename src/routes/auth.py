from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from loguru import logger

from services.auth_service import create_access_token
from db.user import get_current_user, save_user, authenticate_user
from schemas.auth import SignupRequest, SignupResponse, SigninResponse, User


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=SigninResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    logger.info(form_data.username)
    logger.info(form_data.password)

    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return SigninResponse(**user, token=access_token)


@router.get("/me", response_model=User)
async def read_user_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.post("/signup", response_model=SignupResponse)
async def signup(user: SignupRequest):
    user.firstName = user.firstName.capitalize().strip()
    user.lastName = user.lastName.upper().strip()
    user_saved = await save_user(user)
    if not user_saved:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": "User already exists"},
        )
    return SignupResponse(
        id=str(user_saved.id),
        username=user_saved.username,
        settings=user_saved.settings,
    )
