from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime

from domain.entities.image_entity import Image
from domain.repositories.image_repository import ImageRepository
from infrastructure.db.models.image_model import ImageModel
from infrastructure.mappers.image_mapper import ImageMapper


class ImageRepositoryImpl(ImageRepository):
    """Implementación real del repositorio de imágenes usando SQLAlchemy"""

    def __init__(self, db_session: Session):
        self.db = db_session

    def save(self, image: Image) -> Image:
        image_model = ImageMapper.to_model(image)
        self.db.add(image_model)
        self.db.commit()
        self.db.refresh(image_model)
        return ImageMapper.to_entity(image_model)

    def find_by_id(self, image_id: UUID) -> Optional[Image]:
        image_model = self.db.query(ImageModel).filter(ImageModel.id == image_id, ImageModel.is_deleted == False).first()
        return ImageMapper.to_entity(image_model) if image_model else None

    def find_by_user_id(self, user_id: UUID) -> List[Image]:
        images = self.db.query(ImageModel).filter(ImageModel.user_id == user_id).all()
        return [ImageMapper.to_entity(img) for img in images]

    def delete(self, image_id: UUID) -> None:
        image_model = self.db.query(ImageModel).filter(ImageModel.id == image_id).first()
        if image_model:
            self.db.delete(image_model)
            self.db.commit()

    def list_by_user_id(self, user_id: UUID) -> List[Image]:
        """Devuelve todas las imágenes asociadas a un usuario."""
        # Filtra las imágenes por el ID del usuario y las devuelve como una lista de entidades.
        models = self.db.query(ImageModel).filter(ImageModel.user_id == user_id, ImageModel.is_deleted == False).all() # Devuelve todos los modelos de imagen asociados al usuario
        
        # Utiliza el mapper para convertir los modelos a entidades de dominio.
        return [ImageMapper.to_entity(model) for model in models] # Devuelve una lista de entidades Image a partir de los modelos obtenidos

    def get_by_id(self, image_id: UUID) -> Optional[Image]:    
        """Busca una imagen por su ID y devuelve la entidad Image.""" # Busca una imagen por su ID (Devuelve la url temporal del bucket privado)
        # Busca el modelo de imagen por ID y lo convierte a entidad de dominio.
        model = self.db.query(ImageModel).filter(ImageModel.id == image_id).first()
        if not model:
            return None
        return ImageMapper.to_entity(model)


    def soft_delete(self, image_id: UUID) -> bool:
        model = self.db.query(ImageModel).filter(ImageModel.id == image_id).first()
        if not model:
            return False
        model.is_deleted = True
        model.deleted_at = datetime.utcnow()
        self.db.commit()
        return True
    

    def find_deleted_by_user_id(self, user_id: UUID) -> List[Image]:
        models = (
            self.db.query(ImageModel)
            .filter(ImageModel.user_id == user_id, ImageModel.is_deleted == True)
            .all()
        )
        return [ImageMapper.to_entity(m) for m in models]