from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from domain.entities.user_entity import User
from domain.repositories.user_repository import UserRepository #Importamos la interfaz UserRepository
from infrastructure.db.models.user_model import UserModel


# Desarrollamos la lógica de los métodos definidos en la interfaz UserRepository
# Esta clase implementa la interfaz UserRepository y proporciona la lógica para interactuar con la base de datos usando SQLAlchemy.
class UserRepositoryImpl(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        user_model = UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            password=user.password,
            is_admin=user.is_admin,
            created_at=user.created_at,
        )
        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)
        return self._to_entity(user_model)

    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        user_model = self.session.query(UserModel).filter_by(id=user_id).first()
        return self._to_entity(user_model) if user_model else None

    def get_by_email(self, email: str) -> Optional[User]:
        user_model = self.session.query(UserModel).filter_by(email=email).first()
        return self._to_entity(user_model) if user_model else None

    def list_all(self) -> List[User]:
        users = self.session.query(UserModel).all()
        return [self._to_entity(u) for u in users]

    def delete(self, user_id: uuid.UUID) -> None:
        self.session.query(UserModel).filter_by(id=user_id).delete()
        self.session.commit()

    def _to_entity(self, user_model: UserModel) -> User:   # Método privado para convertir el modelo en entidad
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            password=user_model.password,
            is_admin=user_model.is_admin,
            created_at=user_model.created_at,
        )
