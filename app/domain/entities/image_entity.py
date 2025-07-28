from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

@dataclass
class Image:
    id: UUID
    user_id: UUID
    file_name: str
    url: str
    created_at: Optional[datetime] = None
