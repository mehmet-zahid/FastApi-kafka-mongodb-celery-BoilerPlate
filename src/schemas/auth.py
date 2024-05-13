from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    id: str
    username: str
    email: Optional[str] = ""
    firstName: Optional[str] = ""
    lastName: Optional[str] = ""
    settings: dict | None = None


class SigninResponse(BaseModel):
    id: str
    username: str
    token: str


class SignupResponse(BaseModel):
    id: str
    username: str
    settings: dict | None = None


class SignupRequest(BaseModel):
    username: str
    password: str
    email: Optional[str] = ""
    firstName: Optional[str] = ""
    lastName: Optional[str] = ""
