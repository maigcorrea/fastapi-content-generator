from domain.entities.user_entity import User
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
            is_admin=False,
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
