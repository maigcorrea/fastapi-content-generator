### **🛡️ Protección de endpoints FastAPI OAuth2 with Password (and hashing), Bearer with JWT tokens**
El flujo de contraseñas es una de las formas (flujos) definidas en OAuth2 para gestionar la seguridad y la autenticación.

- OAuth2 se diseñó para que el backend o la API fueran independientes del servidor que autentica al usuario.

- Pero en este caso, la misma aplicación FastAPI gestionará la API y la autenticación.

🔎 Revisémoslo desde esta perspectiva simplificada:

- El usuario escribe el nombre de usuario y la contraseña en el frontend y pulsa Intro.
- El frontend (que se ejecuta en el navegador del usuario) envía ese nombre de usuario y contraseña a una URL específica en nuestra API (declarada con tokenUrl="token").
- La API comprueba ese nombre de usuario y contraseña y responde con un token JWT.
- El frontend almacena ese token JWT temporalmente en algún lugar.
- El usuario hace clic en el frontend para ir a otra sección de la aplicación web frontend.
- El frontend necesita obtener más datos de la API.
- Pero necesita autenticación para ese endpoint específico. Para autenticarse con nuestra API, se envía un encabezado "Autorización" con el valor "Bearer" más el token.
- Si el token contiene "foobar", el contenido del encabezado "Autorización" sería: "Bearer foobar".

**🔄 Flujo resumido**
El frontend envía usuario/contraseña → obtiene token JWT → lo usa en futuras peticiones.

### 🔐 Flujo de autenticación con OAuth2 + Con flujo Password JWT en FastAPI (implementación real)
**1. Generación del token JWT🔑**

En el endpoint ``` /users/login ``` después de validar las credenciales con ```pwd_context.verify()```, se genera un token JWT que incluye el user_id como sub:

```python
jwt.encode({"sub": str(user.id)}, SECRET_KEY, algorithm=ALGORITHM)
```
En este caso el token también incluye la fecha de expiración: 

- El usuario envía su email y contraseña.

- ```LoginUserUseCase``` verifica credenciales usando ```pwd_context.verify()```.

- Si son válidas, genera un JWT usando ```jose.jwt.encode()``` con:

- **sub**: ID del usuario

- **exp**: fecha de expiración

- Se devuelve al frontend junto con otros datos relevantes

Código completo:
```python
    def execute(self, dto: LoginUserDto) -> dict:
        user = self.user_repo.get_by_email(dto.email)

        if not user or not pwd_context.verify(dto.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        payload = {
            "sub": str(user.id),
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }

        # Generar el token JWT

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return {
            "access_token": token,
            "is_admin": user.is_admin
        }
```

**2. Almacenar y enviar el token📤**

- El frontend guarda el token (en localStorage o memory).

- En cada petición protegida, lo incluye como header:

```
Authorization: Bearer <token>
```

**3. Validación de endpoints con dependencia get_current_user🧐**
- Extrae el token de la cabecera ```Authorization: Bearer <token>``` con ```OAuth2PasswordBearer```

- Decodifica el JWT

- Obtiene el user_id del payload (sub)

- Llama al repo para obtener el usuario real (Busca el usuario en la base de datos)

- Lanza un ```error 401``` si algo falla

- Si todo está bien, devuelve el ```current_user```

```python
def get_current_user(token: str = Depends(oauth2_scheme), ...):
    ...
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    ...
```

Código completo:
```python
def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repository)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = user_repo.get_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user
```

**4. Validación de endpoints con restricción por rol mediante la dependencia get_current_user🧐**

- Depende de get_current_user

- Verifica que current_user.is_admin sea True

- Lanza 403 Forbidden si no lo es

```python
def get_current_admin_user(current_user = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user
```

Código completo:
```python
def get_current_admin_user(current_user = Depends(get_current_user)):
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return current_user
```

#### 🧪 Ejemplo de uso en rutas

```python
@router.get("/me")
def get_profile(current_user = Depends(get_current_user)):
    return current_user

@router.get("/admin-only")
def admin_route(current_user = Depends(get_current_admin_user)):
    return {"message": "Solo accesible por administradores"}
```

#### 🧱 Estructura del sistema
La implementación se basa en una arquitectura por capas:

- use_cases/login_user_use_case.py: genera y devuelve el token JWT

- auth_dependencies.py: contiene las dependencias get_current_user y get_current_admin_user

- user_router.py: expone las rutas /users/login, /users/ y protege rutas con Depends(get_current_user)

- user_repository_impl.py: accede a los datos reales del usuario (por email o ID)

- .env: contiene SECRET_KEY, ALGORITHM y ACCESS_TOKEN_EXPIRE_MINUTES

#### 🔑 Autenticación en Swagger
Gracias a ```OAuth2PasswordBearer(tokenUrl="/users/login")```, FastAPI añade **automáticamente** un botón “Authorize” en la documentación Swagger para probar autenticación con token Bearer.

```python
#En las dependencias
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
```

- Haz clic en "Authorize"

- Introduce usuario y contraseña

- FastAPI obtendrá el token y lo usará en los headers automáticamente en los endpoints protegidos

(Adjuntar imagen de swagger)

#### ✅ Resultado
✅ Token seguro con expiración (exp)

✅ Verificación automática en cada endpoint con Depends

✅ Protección opcional para administradores

✅ Integración directa con Swagger y frontend