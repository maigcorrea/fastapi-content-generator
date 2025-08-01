import random
from datetime import datetime, timedelta

from domain.repositories.pending_user_repository import PendingUserRepository
from infrastructure.dto.resend_code_dto import ResendCodeDto
from infrastructure.mail.email_service import EmailService


class ResendVerificationCodeUseCase:
    def __init__(self, pending_user_repo: PendingUserRepository, email_service: EmailService):
        self.pending_user_repo = pending_user_repo
        self.email_service = email_service

    def execute(self, dto: ResendCodeDto):
        pending_user = self.pending_user_repo.get_by_email(dto.email)
        if not pending_user:
            raise ValueError("No hay un registro pendiente con ese email")

        # Comprobamos caducidad
        if pending_user.expires_at < datetime.utcnow():
            self.pending_user_repo.delete(pending_user.id)
            raise ValueError("El código ya ha caducado, regístrate de nuevo")

        # Generar nuevo código y caducidad
        new_code = f"{random.randint(100000, 999999)}"
        pending_user.verification_code = new_code
        pending_user.expires_at = datetime.utcnow() + timedelta(minutes=5)

        # Guardar cambios (Uasamos el método update del repositorio en vez de create, porque ese usuario ya existe dentro de pending_users (su id ya está registrado), sólo hay que actualizar su código y la fecha de expiración de este ya que es nuevo)
        self.pending_user_repo.update(pending_user)

        # Reenviar email
        self.email_service.send_verification_email(pending_user.email, new_code)

        return {"message": "Nuevo código enviado correctamente"}
