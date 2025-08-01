from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID  # Si usas PostgreSQL
from datetime import datetime
import uuid

from infrastructure.db.db_config import Base

class PendingUser(Base):
    __tablename__ = "pending_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    verification_code = Column(String(6), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
