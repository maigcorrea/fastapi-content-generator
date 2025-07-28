import os
import shutil
from uuid import uuid4
from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session

# Infraestructura
from infrastructure.db.db_config import get_db
from infrastructure.db.repositories.image_repository_impl import ImageRepositoryImpl
from infrastructure.dto.image_dto import ImageCreateDTO, ImageResponseDTO
from infrastructure.mappers.image_mapper import ImageMapper
from infrastructure.auth.auth_dependencies import get_current_user

# Casos de uso
from application.use_cases.image_use_cases.upload_image_use_case import UploadImageUseCase


router = APIRouter(prefix="/images", tags=["Images"])

# Carpeta local para pruebas
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=ImageResponseDTO)
def upload_image(
    file: UploadFile,
    current_user=Depends(get_current_user),   # usuario autenticado
    db: Session = Depends(get_db)  # sesión de base de datos
):
    # 1. Guardar el archivo en local
    file_extension = os.path.splitext(file.filename)[1]
    new_file_name = f"{uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, new_file_name)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando el archivo: {e}")

    # 2. Construir el DTO para el caso de uso
    dto = ImageCreateDTO(
        file_name=new_file_name,
        url=f"/{UPLOAD_DIR}/{new_file_name}",  # URL local de momento
        user_id=current_user.id
    )

    # 3. Llamar al caso de uso
    image_repository: ImageRepository = ImageRepositoryImpl(db)
    use_case = UploadImageUseCase(image_repository)
    image_entity = use_case.execute(dto)

    # 4. Transformar a DTO de respuesta y devolver
    return ImageMapper.to_response_dto(image_entity)
