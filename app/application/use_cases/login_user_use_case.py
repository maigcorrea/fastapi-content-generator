from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from domain.repositories.user_repository import UserRepository
from infrastructure.dto.user_dto import LoginUserDto
from fastapi import HTTPException

import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno desde .env

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret") # Clave secreta para firmar los tokens JWT
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Algoritmo de encriptación
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")) # Tiempo de expiración del token en minutos

print(f"Loaded SECRET_KEY: {SECRET_KEY}")
print(f"Loaded ALGORITHM: {ALGORITHM}")
print(f"Token expires in: {ACCESS_TOKEN_EXPIRE_MINUTES} minutes")

# Configuración del contexto de encriptación de contraseñas
# Usamos bcrypt como el algoritmo de encriptación para las contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, dto: LoginUserDto) -> dict: # dict especifica que el método devuelve un diccionario con el token y otros datos
        # Primero, buscamos al usuario por su email
        # Si no existe o la contraseña no coincide, lanzamos una excepción HTTP 401
        user = self.user_repo.get_by_email(dto.email)

        if not user or not pwd_context.verify(dto.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Si las credenciales son válidas, generamos un token JWT
        # El payload del token puede incluir información como el ID del usuario y la fecha de expiración
        payload = {
            "sub": str(user.id),
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }

        # Generar el token JWT
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return {
            "access_token": token,
            "is_admin": user.is_admin
        }
