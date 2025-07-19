from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.db.db_config import SessionLocal
from app.infrastructure.db.repositories.user_repository_impl import UserRepositoryImpl
from app.application.use_cases.create_user_use_case import CreateUserUseCase
from app.infrastructure.dto.user_dto import CreateUserDto, UserResponseDto

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
