from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.image_entity import Image


class ImageRepository(ABC):
    """Puerto del repositorio de imágenes"""

    @abstractmethod
    def save(self, image: Image) -> Image:
        """Guarda una imagen en la base de datos"""
        pass

    @abstractmethod
    def find_by_id(self, image_id: UUID) -> Optional[Image]:
        """Busca una imagen por su ID"""
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: UUID) -> List[Image]:
        """Obtiene todas las imágenes de un usuario"""
        pass

    @abstractmethod
    def delete(self, image_id: UUID) -> None:
        """Elimina una imagen"""
        pass
