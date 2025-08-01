from domain.entities.user_entity import User
from domain.entities.pending_user import PendingUser
from infrastructure.dto.user_dto import CreateUserDto, UserResponseDto
from uuid import uuid4
from datetime import datetime
from infrastructure.security.password import hash_password

class UserMapper:

    @staticmethod
    def from_create_dto(dto: CreateUserDto) -> User:
        return User(
            id=uuid4(),
            username=dto.username,
            email=dto.email,
            password=hash_password(dto.password),  # ← ahora se encripta
            is_admin=dto.is_admin, # Esto debería ser False para que se meta por defecto, por si alguien desde el json que se envía desde el frontend cuela un true en el is_admin, pero de momento para probar la app y que me deje meter admin desde swagger lo dejo así
            created_at=datetime.utcnow()
        )

    @staticmethod
    def to_response_dto(user: User) -> UserResponseDto:
        return UserResponseDto(
            id=user.id,
            username=user.username,
            email=user.email,
            is_admin=user.is_admin,
            created_at=user.created_at
        )

    @staticmethod
    def from_pending_user_entity(pending: PendingUser) -> User:
        return User(
            id=pending.id,
            username=pending.username,
            email=pending.email,
            password=pending.password_hash,
            is_admin=False,
            created_at=datetime.utcnow()
        )