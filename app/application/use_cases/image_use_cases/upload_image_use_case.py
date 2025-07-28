from domain.repositories.image_repository import ImageRepository
from infrastructure.dto.image_dto import ImageCreateDTO
from domain.entities.image_entity import Image
from infrastructure.mappers.image_mapper import ImageMapper
import uuid
from datetime import datetime


class UploadImageUseCase:
    """Caso de uso para subir y registrar una imagen"""

    def __init__(self, image_repository: ImageRepository):
        self.image_repository = image_repository

    def execute(self, dto: ImageCreateDTO) -> Image:
        # Convertir el DTO en entidad de dominio
        image_entity = ImageMapper.from_create_dto(dto)

        # Asignar ID y fecha de creación si no existen
        image_entity.id = uuid.uuid4()
        image_entity.created_at = datetime.utcnow()

        # Guardar en la base de datos
        image_entity = self.image_repository.save(image_entity)

        return image_entity
