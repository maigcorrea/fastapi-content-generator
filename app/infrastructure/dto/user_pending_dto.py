from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid


class CreatePendingUserDto(BaseModel):
    username: str
    email: EmailStr
    password: str   # sin hashear todavía, eso lo hará el caso de uso


class PendingUserResponseDto(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    created_at: datetime
    expires_at: datetime
