from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.user_entity import User
import uuid

class UserRepository(ABC):

    @abstractmethod 
    def create(self, user: User) -> User: # This method should create a new user in the repository.
        pass # Este método debe existir en todas las subclases (@abstractmethod). Pero como es abstracto, no tiene implementación aquí, así que usamos pass como marcador de posición para que el código sea válido. Deja un espacio vacío para que sea válido.

    @abstractmethod
    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]: # El método debe devolver un usuario por su ID o None si no se encuentra, por eso pone Optional.
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def list_all(self) -> List[User]:
        pass

    @abstractmethod
    def delete(self, user_id: uuid.UUID) -> None:
        pass

#Anotaciones
# - `@abstractmethod`: Es un decorador que marca un método como obligatorio de implementar en cualquier clase que herede de UserRepository. Si una subclase no implementa todos los métodos marcados como @abstractmethod, no se podrá instanciar.

# La -> indica qué tipo devuelve ese método
# -> User significa que ese método debe devolver un objeto del tipo User

# -> Optional[User] significa que puede devolver un User o None

# -> List[User] indica que devolverá una lista de objetos User

# -> None indica que no devuelve nada

# - `Optional[User]`: This indicates that the method may return a `User` object or `None` if no user is found.
# - `List[User]`: This indicates that the method returns a list of `User` objects.
# - `uuid.UUID`: This is the type for the user ID, which is expected to be a UUID.
# - `user: User`: This parameter indicates that the method expects a `User` object to be passed when creating a new user.


# self es una referencia al objeto actual (la instancia de la clase). Ejemplo: si tienes una clase `Coche`, dentro de sus métodos puedes usar `self` para referirte a la instancia específica de `Coche` que estás manipulando.
# Ejemplo de Self:
# class Coche:
#     def __init__(self, marca):
#         self.marca = marca  # Aquí self.marca se refiere al atributo marca de la instancia actual de Coche
#     def mostrar_marca(self):
#         return self.marca  # Aquí self se usa para acceder al atributo marca de la instancia actual
# Otro ejemplo de self:
# class Persona:
#     def saludar(self):
#         print("Hola")

# p = Persona()
# p.saludar()  # Aquí `self` dentro de saludar() es la instancia `p`


