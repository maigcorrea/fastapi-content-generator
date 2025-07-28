from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

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
        image_model = self.db.query(ImageModel).filter(ImageModel.id == image_id).first()
        return ImageMapper.to_entity(image_model) if image_model else None

    def find_by_user_id(self, user_id: UUID) -> List[Image]:
        images = self.db.query(ImageModel).filter(ImageModel.user_id == user_id).all()
        return [ImageMapper.to_entity(img) for img in images]

    def delete(self, image_id: UUID) -> None:
        image_model = self.db.query(ImageModel).filter(ImageModel.id == image_id).first()
        if image_model:
            self.db.delete(image_model)
            self.db.commit()
