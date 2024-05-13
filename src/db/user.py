from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from loguru import logger
from motor.core import AgnosticCollection
from datetime import datetime

from config import mongo_config
from mongohelper import mongoo_instance as mymongoo
from models.user import UserModel
from schemas.auth import SignupRequest, User
from services.auth_service import decode_token, get_password_hash, verify_password

# OAuth2PasswordBearer for token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def query_user(username: str) -> dict | None:
    coll: AgnosticCollection = mymongoo.get_collection(mongo_config.DB_NAME, "users")
    # query with username or email property
    user_query_res = await coll.find_one(
        {"$or": [{"username": username}, {"email": username}]}
    )
    if not user_query_res:
        return None
    id = str(user_query_res.pop("_id"))
    user_query_res["id"] = id
    return user_query_res


async def save_user(user_signup: SignupRequest) -> UserModel | bool:
    # Check if user already exists
    user = await UserModel.find_one({"username": user_signup.username})
    if user:
        # User already exists, we cannot create another one with the same username
        return False
    # User does not exist, we can create a new one

    # Hash the password
    hashed_password = get_password_hash(user_signup.password)
    user = UserModel(
        username=user_signup.username,
        password=hashed_password,
        email=user_signup.email,
        firstName=user_signup.firstName,
        lastName=user_signup.lastName,
        createdAt=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    await user.save()
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload, message = decode_token(token)
    logger.info(payload)
    logger.info(message)

    if payload is None:
        credentials_exception.detail = message
        raise credentials_exception

    username: str = payload.get("sub")
    logger.info(username)
    if username is None:
        raise credentials_exception

    user = await query_user(username)
    if user is None:
        credentials_exception.detail = "User not found"
        raise credentials_exception
    return User(**user)


async def authenticate_user(username: str, password: str) -> dict | None:
    user_data = await query_user(username)
    if not user_data:
        return None
    if not verify_password(password, user_data["password"]):
        return None
    return user_data
