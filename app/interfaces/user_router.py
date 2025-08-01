from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from infrastructure.db.db_config import SessionLocal
from infrastructure.db.db_config import get_db
from infrastructure.db.repositories.user_repository_impl import UserRepositoryImpl
from application.use_cases.create_user_use_case import CreateUserUseCase
from infrastructure.dto.user_dto import CreateUserDto, UserResponseDto
from infrastructure.auth.auth_dependencies import get_current_user
from infrastructure.auth.auth_dependencies import get_current_admin_user

# Importar el caso de uso de login y el DTO y el contexto de encriptación
from application.use_cases.login_user_use_case import LoginUserUseCase
from infrastructure.dto.user_dto import LoginUserDto
from passlib.context import CryptContext

# Este contexto se usará luego para hashear contraseñas también
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# mail
from infrastructure.dto.user_pending_dto import CreatePendingUserDto
from infrastructure.dto.verify_user_dto import VerifyUserDto
from infrastructure.dto.resend_code_dto import ResendCodeDto
from application.use_cases.verify_pending_user_use_case import VerifyPendingUserUseCase
from application.use_cases.create_pending_user_use_case import CreatePendingUserUseCase
from application.use_cases.resend_verification_code_use_case import ResendVerificationCodeUseCase
from infrastructure.db.repositories.pending_user_repository_impl import PendingUserRepositoryImpl
from infrastructure.mail.email_service import EmailService


# Crear el router para manejar las rutas relacionadas con usuarios
router = APIRouter(prefix="/users", tags=["Users"])

# Dependency para obtener la sesión de DB
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@router.post("/", response_model=UserResponseDto, status_code=201)
# Registrar a un usuario directamente, sin verificación de email (Este endpoint al final lo tendré que quitar, pero para pruebas directas sin tener que meter el código de verificación está bien)
def create_user(dto: CreateUserDto, db: Session = Depends(get_db)): #Proteger endpoint: current_user=Depends(get_current_user); current_user es para asegurarnos de que el usuario que crea otro usuario está autenticado
    user_repo = UserRepositoryImpl(db)
    use_case = CreateUserUseCase(user_repo)

    # Opcional: comprobar si el email ya existe
    if user_repo.get_by_email(dto.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Si quieres que los usuarios normales no puedan forzar is_admin=True: (Complementar con el current_user=Depends(get_current_user)) NO IMPLEMENTADO DE MOMENTO PARA LAS PRUEBAS
    # if not current_user.is_admin:
    #     dto.is_admin = False  # 🔐 blindaje, un usuario normal no puede autoproclamarse admin ni crear un admin

    return use_case.execute(dto)

# Endpoint para crear un usuario admin (solo accesible por admins)
# Aquí se asume que el usuario que llama a este endpoint es un admin, por lo que no se necesita la validación de is_admin en el DTO
# @router.post("/admin/users", response_model=UserResponseDto)
# def create_admin_user(
#     dto: CreateUserDto,
#     db: Session = Depends(get_db),
#     #current_admin=Depends(get_current_admin_user)  # Solo admins entran aquí
# ):
#     user_repo = UserRepositoryImpl(db)
#     use_case = CreateUserUseCase(user_repo)

#     if user_repo.get_by_email(dto.email):
#         raise HTTPException(status_code=400, detail="Email already registered")

#     return use_case.execute(dto)


@router.post("/login", tags=["Auth"])
def login_user(dto: LoginUserDto, db: Session = Depends(get_db)):
    user_repo = UserRepositoryImpl(db)
    use_case = LoginUserUseCase(user_repo) # Aquí se crea el caso de uso de login
    result = use_case.execute(dto) # Aquí se ejecuta el caso de uso de login
    
    # Retornar el token JWT si el email/contraseña son correctos, y si el usuario es admin
    return {"access_token": result["access_token"], "token_type": "bearer", "is_admin": result["is_admin"] }


# Endpoint para registrar un usuario pendiente (para verificación por email - enviar código de verificación)
@router.post("/register-pending")
def register_pending_user(dto: CreatePendingUserDto, db: Session = Depends(get_db)):
    repo = PendingUserRepositoryImpl(db)
    email_service = EmailService()
    use_case = CreatePendingUserUseCase(repo, email_service)
    return use_case.execute(dto)


# Endpoint para verificar un usuario pendiente (confirmación de email - confirmación de código de verificación)
@router.post("/verify")
def verify_user(dto: VerifyUserDto, db: Session = Depends(get_db)):
    pending_repo = PendingUserRepositoryImpl(db)
    user_repo = UserRepositoryImpl(db)
    use_case = VerifyPendingUserUseCase(pending_repo, user_repo)
    return use_case.execute(dto)


# Endpoint para volver a enviar el códdigo en caso de que no se haya recibido
@router.post("/resend-code")
def resend_code(dto: ResendCodeDto, db: Session = Depends(get_db)):
    repo = PendingUserRepositoryImpl(db)
    email_service = EmailService()
    use_case = ResendVerificationCodeUseCase(repo, email_service)
    return use_case.execute(dto)