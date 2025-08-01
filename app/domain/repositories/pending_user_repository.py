import uuid
from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

from domain.entities.pending_user import PendingUser
from infrastructure.db.models.pending_user_model import PendingUser as PendingUserModel


class PendingUserRepository(ABC):
    """Puerto (interfaz) para el repositorio de PendingUser"""

    @abstractmethod
    def create(self, pending_user: PendingUser) -> PendingUser:
        """Guardar un nuevo pending_user en la base de datos"""
        pass

    @abstractmethod
    def get_by_email_and_code(self, email: str, code: str) -> Optional[PendingUser]:
        """Buscar un pending_user por email y código"""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[PendingUser]:
        """Buscar un pending_user solo por email"""
        pass

    @abstractmethod
    def delete(self, pending_user_id: uuid.UUID) -> None:
        """Eliminar un pending_user (tras verificarlo o si expira)"""
        pass

    @abstractmethod
    def delete_expired(self, now: datetime) -> int:
        """Eliminar registros caducados (expires_at < now)"""
        pass

    @abstractmethod
    def _to_entity(self, pending_user_model: PendingUserModel) -> PendingUser:
        """Convertir un modelo PendingUser a entidad PendingUser"""
        pass    

    @abstractmethod
    def update(self, pending_user: PendingUser) -> PendingUser:
        """Actualizar código y expiración de un pending_user existente"""
        pass
