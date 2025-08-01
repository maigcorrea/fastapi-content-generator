from sqlalchemy.orm import Session
from typing import Optional
import uuid
from datetime import datetime


from domain.entities.pending_user import PendingUser
from domain.repositories.pending_user_repository import PendingUserRepository
from infrastructure.db.models.pending_user_model import PendingUser as PendingUserModel


class PendingUserRepositoryImpl(PendingUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, pending_user: PendingUser) -> PendingUser:
        pending_user_model = PendingUserModel(
            id=pending_user.id or uuid.uuid4(),
            username=pending_user.username,
            email=pending_user.email,
            password_hash=pending_user.password_hash,
            verification_code=pending_user.verification_code,
            created_at=pending_user.created_at,
            expires_at=pending_user.expires_at,
        )
        self.session.add(pending_user_model)
        self.session.commit()
        self.session.refresh(pending_user_model)
        return self._to_entity(pending_user_model)

    def get_by_email_and_code(self, email: str, code: str) -> Optional[PendingUser]:
        pending_user_model = (
            self.session.query(PendingUserModel)
            .filter_by(email=email, verification_code=code)
            .first()
        )
        # Validamos si está caducado
        if pending_user_model and pending_user_model.expires_at > datetime.utcnow():
            return self._to_entity(pending_user_model)
        return None

    def get_by_email(self, email: str) -> Optional[PendingUser]:
        pending_user_model = self.session.query(PendingUserModel).filter_by(email=email).first()
        return self._to_entity(pending_user_model) if pending_user_model else None

    def delete(self, pending_user_id: uuid.UUID) -> None:
        self.session.query(PendingUserModel).filter_by(id=pending_user_id).delete()
        self.session.commit()

    def delete_expired(self, now: datetime) -> int:
        result = (
            self.session.query(PendingUserModel).filter(PendingUserModel.expires_at < now).delete()
        )
        self.session.commit()  
        return result # número de registros eliminados

    def _to_entity(self, pending_user_model: PendingUserModel) -> PendingUser:
        return PendingUser(
            id=pending_user_model.id,
            username=pending_user_model.username,
            email=pending_user_model.email,
            password_hash=pending_user_model.password_hash,
            verification_code=pending_user_model.verification_code,
            created_at=pending_user_model.created_at,
            expires_at=pending_user_model.expires_at,
        )

# Método para actualizar el código y la expiración de un pending_user existente (cuabdo se reenvía el código de nuevo)
    def update(self, pending_user: PendingUser) -> PendingUser:
        model = self.session.query(PendingUserModel).filter_by(id=pending_user.id).first()
        if model:
            model.verification_code = pending_user.verification_code
            model.expires_at = pending_user.expires_at
            self.session.commit()
            self.session.refresh(model)
            return self._to_entity(model)
        else:
            raise ValueError("Pending user not found")
