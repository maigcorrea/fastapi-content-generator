from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

# This module defines the User entity for the application.
# It includes fields for user identification, authentication, and metadata.
@dataclass
class User:
    id: uuid.UUID
    username: str
    email: str
    password: str
    is_admin: bool = False
    created_at: Optional[datetime] = None