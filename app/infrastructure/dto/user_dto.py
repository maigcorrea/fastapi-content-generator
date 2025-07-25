from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class CreateUserDto(BaseModel):
    username: str
    email: EmailStr
    password: str  # ← en producción hashearlo antes de guardar
    is_admin: bool = False #Tendría que quitarlo en realidad pero es mientras se prueba la app para añadir admins desde swagger

class UserResponseDto(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_admin: bool
    created_at: datetime

# Login DTO - Establece el formato para el inicio de sesión
class LoginUserDto(BaseModel):
    email: EmailStr
    password: str