from datetime import datetime

from domain.repositories.pending_user_repository import PendingUserRepository
from domain.repositories.user_repository import UserRepository
from infrastructure.dto.verify_user_dto import VerifyUserDto
from infrastructure.mappers.user_mapper import UserMapper   # ya lo tienes hecho para users
from infrastructure.mappers.user_pending_mapper import PendingUserMapper


class VerifyPendingUserUseCase:
    def __init__(self, pending_user_repo: PendingUserRepository, user_repo: UserRepository):
        self.pending_user_repo = pending_user_repo
        self.user_repo = user_repo

    def execute(self, dto: VerifyUserDto):
        # Buscar el usuario pendiente por email y código
        pending_user = self.pending_user_repo.get_by_email_and_code(dto.email, dto.code)
        if not pending_user:
            raise ValueError("Código incorrecto o caducado")

        # Crear usuario definitivo en la tabla users usando el UserMapper
        user_entity = UserMapper.from_pending_user_entity(pending_user)  
        self.user_repo.create(user_entity)

        # Borrar el registro temporal
        self.pending_user_repo.delete(pending_user.id)

        return {"message": "Usuario verificado y registrado correctamente"}
