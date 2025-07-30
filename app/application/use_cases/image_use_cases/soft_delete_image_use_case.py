from uuid import UUID
from fastapi import HTTPException
from domain.repositories.image_repository import ImageRepository

class SoftDeleteImageUseCase:
    """Marca una imagen como eliminada (soft delete)"""

    def __init__(self, image_repository: ImageRepository):
        self.image_repository = image_repository

    def execute(self, image_id: UUID) -> bool:
        deleted = self.image_repository.soft_delete(image_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Imagen no encontrada")
        return True
