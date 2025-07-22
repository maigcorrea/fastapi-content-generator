from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from infrastructure.db.db_config import SessionLocal
from infrastructure.db.repositories.user_repository_impl import UserRepositoryImpl
from application.use_cases.create_user_use_case import CreateUserUseCase
from infrastructure.dto.user_dto import CreateUserDto, UserResponseDto

# Importar el caso de uso de login y el DTO y el contexto de encriptación
from application.use_cases.login_user_use_case import LoginUserUseCase
from infrastructure.dto.user_dto import LoginUserDto
from passlib.context import CryptContext

# Este contexto se usará luego para hashear contraseñas también
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



# Crear el router para manejar las rutas relacionadas con usuarios
router = APIRouter(prefix="/users", tags=["Users"])

# Dependency para obtener la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserResponseDto, status_code=201)
def create_user(dto: CreateUserDto, db: Session = Depends(get_db)):
    user_repo = UserRepositoryImpl(db)
    use_case = CreateUserUseCase(user_repo)

    # Opcional: comprobar si el email ya existe
    if user_repo.get_by_email(dto.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    return use_case.execute(dto)


@router.post("/login", tags=["Auth"])
def login_user(dto: LoginUserDto, db: Session = Depends(get_db)):
    user_repo = UserRepositoryImpl(db)
    use_case = LoginUserUseCase(user_repo) # Aquí se crea el caso de uso de login
    token = use_case.execute(dto) # Aquí se ejecuta el caso de uso de login
    
    # Retornar el token JWT si el email/contraseña son correctos
    return {"access_token": token, "token_type": "bearer"}