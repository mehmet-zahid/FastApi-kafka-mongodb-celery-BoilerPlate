from beanie import Document
from typing import Optional


class UserModel(Document):
    username: str
    password: str
    email: str
    firstName: Optional[str]
    lastName: Optional[str]
    settings: dict | None = None
    createdAt: str | None = None
    updatedAt: str | None = None

    # defines the collection name and indexes
    class Settings:
        name = "users"
        indexes = [
            [("username", 1), ("email", 1)],
        ]
