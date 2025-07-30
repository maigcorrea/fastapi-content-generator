from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
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

    @abstractmethod
    def list_by_user_id(self, user_id: UUID) -> List[Image]: # Devuelve una lista de imágenes asociadas a un usuario(Esto servía para bucket público, Antes de implementar la url firmada con Bucket privado)
        """Devuelve todas las imágenes asociadas a un usuario."""
        pass

    @abstractmethod
    def get_by_id(self, image_id: UUID) -> Optional[Image]:   # Busca una imagen por su ID (Devuelve la url temporal del bucket privado)
        pass

    @abstractmethod
    def soft_delete(self, image_id: UUID) -> bool:
        """Marca una imagen como eliminada sin borrarla físicamente."""
        pass   

    @abstractmethod
    def find_deleted_by_user_id(self, user_id: UUID) -> List[Image]:
        """Devuelve imágenes eliminadas (soft delete)"""
        pass

    @abstractmethod
    def restore(self, image_id: UUID) -> None:
        """Restaura una imagen eliminada (soft delete -> activa)"""
        pass

    @abstractmethod
    def find_deleted_before(self, date: datetime) -> List[Image]:
        """Busca imágenes eliminadas antes de una fecha específica"""
        pass

    @abstractmethod
    def hard_delete(self, image_id: UUID):
        """Elimina una imagen de forma permanente"""
        pass