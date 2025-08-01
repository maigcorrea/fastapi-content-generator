import uuid
from domain.entities.pending_user import PendingUser
from infrastructure.db.models.pending_user_model import PendingUser as PendingUserModel
from infrastructure.dto.user_pending_dto import PendingUserResponseDto, CreatePendingUserDto
from infrastructure.security.password import hash_password
from datetime import datetime


class PendingUserMapper:
    @staticmethod
    def to_entity(model: PendingUserModel) -> PendingUser:
        return PendingUser(
            id=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            verification_code=model.verification_code,
            created_at=model.created_at,
            expires_at=model.expires_at,
        )

    @staticmethod
    def to_model(entity: PendingUser) -> PendingUserModel:
        return PendingUserModel(
            id=entity.id or uuid.uuid4(),
            username=entity.username,
            email=entity.email,
            password_hash=entity.password_hash,
            verification_code=entity.verification_code,
            created_at=entity.created_at,
            expires_at=entity.expires_at,
        )

    @staticmethod
    def to_dto(entity: PendingUser) -> PendingUserResponseDto:
        return PendingUserResponseDto(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            created_at=entity.created_at,
            expires_at=entity.expires_at,
        )

    @staticmethod
    def from_create_dto(dto: CreatePendingUserDto, verification_code: str, expires_at: datetime) -> PendingUser:
        return PendingUser(
            id=uuid.uuid4(),
            username=dto.username,
            email=dto.email,
            password_hash=hash_password(dto.password),
            verification_code=verification_code,
            created_at=datetime.utcnow(),
            expires_at=expires_at,
        )