from domain.repositories.image_repository import ImageRepository
from infrastructure.dto.image_dto import ImageCreateDTO
from domain.entities.image_entity import Image
from infrastructure.mappers.image_mapper import ImageMapper
import uuid
from datetime import datetime
from infrastructure.s3.s3_client import s3_client
from config import settings
from fastapi import HTTPException


class UploadImageUseCase:
    """Caso de uso para subir y registrar una imagen"""

    def __init__(self, image_repository: ImageRepository):
        self.image_repository = image_repository

    def execute(self, dto: ImageCreateDTO, file_obj) -> Image:
        # # Convertir el DTO en entidad de dominio
        # image_entity = ImageMapper.from_create_dto(dto)

        # # Asignar ID y fecha de creación si no existen
        # image_entity.id = uuid.uuid4()
        # image_entity.created_at = datetime.utcnow()

        # # Guardar en la base de datos
        # image_entity = self.image_repository.save(image_entity)

        # return image_entity

        """
        Sube la imagen a MinIO/S3 y la registra en la BD.
        :param dto: Datos de la imagen
        :param file_obj: Archivo (file.file de UploadFile)
        """
        # Subir a MinIO/S3
        try:
            s3_client.upload_fileobj(file_obj, settings.minio_bucket, dto.file_name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error subiendo a S3/MinIO: {e}")

        # Construir URL pública (o firmada en futuro)
        dto.url = f"{settings.minio_endpoint}/{settings.minio_bucket}/{dto.file_name}"

        # Mapear a entidad y asignar datos
        image_entity = ImageMapper.from_create_dto(dto)
        image_entity.id = uuid.uuid4()
        image_entity.created_at = datetime.utcnow()

        # Guardar en la base de datos
        return self.image_repository.save(image_entity)