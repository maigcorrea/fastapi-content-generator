from datetime import datetime
from dataclasses import dataclass
import uuid

@dataclass
class PendingUser:
    id: uuid.UUID | None
    username: str
    email: str
    password_hash: str
    verification_code: str
    created_at: datetime
    expires_at: datetime
