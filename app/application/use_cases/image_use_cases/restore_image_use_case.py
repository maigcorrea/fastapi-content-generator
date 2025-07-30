from uuid import UUID
from domain.repositories.image_repository import ImageRepository
from fastapi import HTTPException

class RestoreImageUseCase:
    """Restaura una imagen eliminada (soft delete -> activa)"""

    def __init__(self, image_repository: ImageRepository):
        self.image_repository = image_repository

    def execute(self, image_id: UUID):
        image = self.image_repository.get_by_id(image_id)
        if not image:
            raise HTTPException(status_code=404, detail="Imagen no encontrada")

        if not image.is_deleted:
            raise HTTPException(status_code=400, detail="La imagen ya está activa")

        self.image_repository.restore(image_id)
