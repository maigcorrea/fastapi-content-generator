from typing import List
from uuid import UUID
from domain.repositories.image_repository import ImageRepository
from domain.entities.image_entity import Image

class ListUserImagesUseCase:
    """Caso de uso para listar las imágenes de un usuario autenticado"""

    def __init__(self, image_repo: ImageRepository):
        self.image_repo = image_repo

    def execute(self, user_id: UUID) -> List[Image]:
        return self.image_repo.list_by_user_id(user_id)
