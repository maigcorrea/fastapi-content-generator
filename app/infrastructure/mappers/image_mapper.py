from domain.entities.image_entity import Image
from infrastructure.db.models.image_model import ImageModel
from infrastructure.dto.image_dto import ImageCreateDTO, ImageResponseDTO


class ImageMapper:
    """Convierte entre ImageModel (ORM) ↔ Image (entidad de dominio) ↔ DTO"""

    # -------------------
    # ORM ↔ Entidad de dominio
    # -------------------
    @staticmethod
    def to_entity(model: ImageModel) -> Image:
        return Image(
            id=model.id,
            user_id=model.user_id,
            file_name=model.file_name,
            url=model.url,
            created_at=model.created_at,
            is_deleted=model.is_deleted,       
            deleted_at=model.deleted_at
        )

    @staticmethod
    def to_model(entity: Image) -> ImageModel:
        return ImageModel(
            id=entity.id,
            user_id=entity.user_id,
            file_name=entity.file_name,
            url=entity.url,
            created_at=entity.created_at,
            is_deleted=entity.is_deleted,    
            deleted_at=entity.deleted_at
        )

    # -------------------
    # DTO ↔ Entidad de dominio
    # -------------------
    @staticmethod
    def from_create_dto(dto: ImageCreateDTO) -> Image:
        """Convierte un ImageCreateDTO en una entidad Image"""
        return Image(
            id=None,  # se asignará al guardar
            user_id=dto.user_id,
            file_name=dto.file_name,
            url=dto.url,
            created_at=None
        )

    @staticmethod
    def to_response_dto(entity: Image) -> ImageResponseDTO:
        """Convierte una entidad Image en ImageResponseDTO"""
        return ImageResponseDTO(
            id=entity.id,
            user_id=entity.user_id,
            file_name=entity.file_name,
            url=entity.url,
            created_at=entity.created_at,
            is_deleted=entity.is_deleted
        )
