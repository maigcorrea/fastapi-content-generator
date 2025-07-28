from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class ImageCreateDTO(BaseModel):
    """DTO para crear una imagen (input desde la API)"""
    file_name: str
    url: str
    user_id: UUID


class ImageResponseDTO(BaseModel):
    """DTO para devolver una imagen en la API"""
    id: UUID
    user_id: UUID
    file_name: str
    url: str
    created_at: Optional[datetime]
