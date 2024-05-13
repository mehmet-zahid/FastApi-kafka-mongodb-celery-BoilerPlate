from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from os import getenv
from datetime import datetime, timedelta
from jose import JWTError, jwt, ExpiredSignatureError
from loguru import logger


SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2PasswordBearer for token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Token Operations
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        # logger.info(type(e))
        if isinstance(e, ExpiredSignatureError):
            # logger.error(e)
            return None, "Token has expired"
        elif isinstance(e, JWTError):
            # logger.error(e)
            return None, "Could not validate credentials"
        else:
            # logger.error(e)
            return None, "Could not validate credentials"


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
