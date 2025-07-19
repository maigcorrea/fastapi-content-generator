from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.dto.user_dto import CreateUserDto, UserResponseDto
from app.infrastructure.mappers.user_mapper import UserMapper

class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, dto: CreateUserDto) -> UserResponseDto:
        user_entity = UserMapper.from_create_dto(dto) # Convert DTO to domain entity
        created_user = self.user_repository.create(user_entity) # Save the user using the repository
        return UserMapper.to_response_dto(created_user) # Convert the created entity back to a response DTO


# This use case handles the creation of a user by mapping the DTO to a domain entity,
# using the repository to persist the user, and then mapping the created entity back to a response DTO.
# It abstracts the business logic of user creation, ensuring that the controller or service layer
# does not need to know about the details of how users are created or stored.

# ¿Qué hace este caso de uso?

# Recibe un CreateUserDto (validado por FastAPI/Pydantic)
# Lo convierte en una entidad de dominio con UserMapper
# Lo guarda usando el repositorio
# Devuelve un UserResponseDto (DTO de salida) listo para la API