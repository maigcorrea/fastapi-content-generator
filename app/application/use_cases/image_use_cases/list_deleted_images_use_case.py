from typing import List
from uuid import UUID
from domain.entities.image_entity import Image
from domain.repositories.image_repository import ImageRepository

class ListDeletedImagesUseCase:
    """Devuelve las imágenes eliminadas de un usuario"""

    def __init__(self, image_repository: ImageRepository):
        self.image_repository = image_repository

    def execute(self, user_id: UUID) -> List[Image]:
        return self.image_repository.find_deleted_by_user_id(user_id)
