import random
from datetime import datetime, timedelta

from domain.repositories.pending_user_repository import PendingUserRepository
from infrastructure.dto.user_pending_dto import CreatePendingUserDto, PendingUserResponseDto
from infrastructure.mappers.user_pending_mapper import PendingUserMapper
from infrastructure.mail.email_service import EmailService


class CreatePendingUserUseCase:
    def __init__(self, pending_user_repo: PendingUserRepository, email_service: EmailService):
        self.pending_user_repo = pending_user_repo
        self.email_service = email_service

    def execute(self, dto: CreatePendingUserDto) -> PendingUserResponseDto:
        # 1️⃣ Generar código de verificación (6 dígitos)
        verification_code = f"{random.randint(100000, 999999)}"

        # 2️⃣ Generar fecha de caducidad (15 minutos desde ahora)
        expires_at = datetime.utcnow() + timedelta(minutes=15)

        # 3️⃣ Mapear DTO a entidad usando el mapper
        pending_user = PendingUserMapper.from_create_dto(dto, verification_code, expires_at)

        # 4️⃣ Guardar en el repositorio
        created_user = self.pending_user_repo.create(pending_user)

        # 5️⃣ Enviar el correo con el código
        self.email_service.send_verification_email(created_user.email, verification_code)

        # 6️⃣ Devolver el DTO de respuesta
        return PendingUserMapper.to_dto(created_user)
