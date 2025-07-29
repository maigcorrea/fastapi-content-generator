import os
import shutil
from uuid import uuid4
from typing import List
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
from application.use_cases.image_use_cases.list_user_images_use_case import ListUserImagesUseCase
from application.use_cases.image_use_cases.get_signed_image_url_use_case import GetSignedImageUrlUseCase

# Lo de minIO / S3
from infrastructure.s3.s3_client import s3_client  # 👈 importar el cliente
from config import settings  # si usas un archivo de settings como en pasos anteriores


router = APIRouter(prefix="/images", tags=["Images"])

# Carpeta local para pruebas
# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=ImageResponseDTO)
def upload_image(
    file: UploadFile,
    current_user=Depends(get_current_user),   # usuario autenticado
    db: Session = Depends(get_db)  # sesión de base de datos
):
    # 1. Guardar el archivo en local (Antes de subir a MinIO/S3)
    # file_extension = os.path.splitext(file.filename)[1]
    # new_file_name = f"{uuid4()}{file_extension}"
    # file_path = os.path.join(UPLOAD_DIR, new_file_name)

    # try:
    #     with open(file_path, "wb") as buffer:
    #         shutil.copyfileobj(file.file, buffer)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Error guardando el archivo: {e}")

    # 1. Generar nombre único
    file_extension = os.path.splitext(file.filename)[1]
    new_file_name = f"{uuid4()}{file_extension}"


    # 2. Construir el DTO para el caso de uso (Antes de subir a S3/MinIO)
    # dto = ImageCreateDTO(
    #     file_name=new_file_name,
    #     url=f"/{UPLOAD_DIR}/{new_file_name}",  # URL local de momento
    #     user_id=current_user.id
    # )

     # 2. Construir el DTO con datos base
    dto = ImageCreateDTO(
        file_name=new_file_name,
        url="", # El caso de uso generará la URL final
        user_id=current_user.id
    )

    # 3. Llamar al caso de uso
    image_repository: ImageRepository = ImageRepositoryImpl(db)
    use_case = UploadImageUseCase(image_repository)
    image_entity = use_case.execute(dto, file.file)  # Pasar el archivo como file_obj

    # 4. Transformar a DTO de respuesta y devolver
    return ImageMapper.to_response_dto(image_entity)

# Listar imágenes del usuario autenticado(En caso de que la imagen esté en un bucket público. Imagen no firmada)
@router.get("/me", response_model=List[ImageResponseDTO])
def list_my_images(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = ImageRepositoryImpl(db)
    use_case = ListUserImagesUseCase(repo)
    images = use_case.execute(current_user.id)
    return [ImageMapper.to_response_dto(image) for image in images]


# Devolver una URL firmada para acceder a la imagen (Bucket privado)
@router.get("/image-url/{image_id}")
def get_image_url(image_id: str, db: Session = Depends(get_db)):
    # Buscar la imagen en la BD
    image_repository = ImageRepositoryImpl(db)
    image = image_repository.get_by_id(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    # Generar URL firmada
    use_case = GetSignedImageUrlUseCase()
    signed_url = use_case.execute(image.url)  # image.url ahora es el file_name

    return {"url": signed_url}