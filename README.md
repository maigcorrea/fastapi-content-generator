# Content Generator

Este proyecto es una API de generación de hashtags a partir de imágenes, construida con **FastAPI**, **PostgreSQL**, **Docker** y con estructura de **arquitectura hexagonal (Clean Architecture)**.
Proyecto para aprender Python orientado a IA + web + arquitectura limpia

## Índice
- [Idea resumida como MVP](#-idea-resumida-como-mvp)
- [Tecnologías usadas](#-tecnologías-usadas)
- [Tecnologías sugeridas por capa](#-tecnologías-sugeridas-por-capa)
- [Estructura de carpetas hexagonal con FastAPI](#-estructura-de-carpetas-hexagonal-en-python-inspirada-en-tu-backend-nestjs)
- [Equivalencia de carpetas de FastAPI con Nestjs](#-equivalencias-con-nestjs)
- [Fases del proyecto](#-fases-del-proyecto)
- [Guía de despliegue local con y sin Docker](#-guía-de-despliegue-local---hashtag-generator-api)
- [A tener en cuenta](#-notas-adicionales)
- [Detalles relevantes del proceso de construcción de la App](#detalles-relevantes)
  - [Protección de backend con OAuth2 + JWT (Versión antigua)](https://github.com/maigcorrea/fastapi-content-generator/blob/main/docs/protección_endpoints_backend_OAuth2(Antigua).md)
  - [Protección de backend con Bearer + JWT (Versión actual)](#️-protección-de-endpoints-fastapi-con-bearer--jwt-tokens-httpbearer)
  - [Sistema de Autenticación y Protección de Rutas (Frontend) con context + hook + Layout](#-sistema-de-autenticación-y-protección-de-rutas-frontend-con-context--hook--layout)
  - [Esquema de flujo de subida, obtención de URLs firmadas y renderizado de imagenes (backend+frontend)](#esquema-de-flujo-de-subida-obtención-de-urls-firmadas-y-renderizado-de-imagenes-backendfrontend)
    - [Subida de imagenes a MinIO con estructura compatible para S3](https://github.com/maigcorrea/fastapi-content-generator/blob/main/docs/subida_img_s3.md)
    - [Gestión de imagenes privadas con URLs firmadas (Presigned URLs for private buckets)](https://github.com/maigcorrea/fastapi-content-generator/blob/main/docs/gestión_img_privadas_url_firmadas.md)
  - [Flujo de subida, obtención y renderizado de imágenes desde el frontend](https://github.com/maigcorrea/fastapi-content-generator/blob/main/docs/gestión_img_frontend.md)
  - [Gestión de eliminación de imágenes](#-gestión-de-imágenes-con-soft-delete-papelera-restauración-y-cron-job)
    - [Documentación completa acerca de la gestión de eliminación imagenes mediante soft delete, papelera, restauración de img y cron](https://github.com/maigcorrea/fastapi-content-generator/blob/main/docs/gestión_eliminación_img.md)

- [Licencias y autores](#autores) 

## ✅ Idea resumida como MVP
- Login / Registro de usuarios

- Subida de imagen por parte del usuario

- Selección manual de plataforma o red social para adaptación de hastags/descripciones al formato requerido

- Generador de hashtags (IA: visión por computadora o modelo entrenado o preentrenado) para aprovechar el máximo alcance en la plataforma seleccionada

- Panel de usuario (historial de imágenes subidas y hashtags generados)

- Panel de admin (ver usuarios registrados)

- Base de datos PostgreSQL

- Contenedores Docker

- Arquitectura hexagonal en Python (Clean Architecture con capas separadas: domain, application, infrastructure, interface)

## ✅ Tecnologías usadas

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker + Docker Compose
- Pydantic
- Uvicorn
- WSL (Ubuntu) en Windows (opcional pero recomendado)
- Arquitectura hexagonal
- NextJs
- Muchas más que iré añadiendo

## 🧠 Tecnologías sugeridas por capa
| Capa | Tecnología     |
| :-------- | :------- | 
| `Interfaz`      | `FastAPI (backend API REST) + NextJs (opcional)` |
| `Infraestructura`      | `SQLAlchemy / Tortoise ORM, PostgreSQL, Docker, JWT` |
| `Aplicación`      | `Casos de uso, DTOs (puros Python)` | 
| `Dominio`      | `Entidades puras, sin dependencias` | 
| `IA`      | `Transformers, CLIP, torchvision, YOLO, etc. para extracción de contenido visual o tags` | 

## 🧱 Estructura de carpetas hexagonal en Python (inspirada en tu backend NestJS)
```
project/
│
├── app/                        # Backend FastAPI
│   ├── domain/                 # Entidades y puertos
│   │   ├── entities/
│   │   ├── repositories/         # Equivalente a /ports en NestJs
│   │   └── services/
│   ├── application/           # Casos de uso
│   │   └── use_cases/
│   ├── infrastructure/        # Implementaciones reales
│   │   ├── db/ (models, SQLAlchemy) # Acceso a la bd
|   |   |    ├── models/         # Modelos ORM (SQLAlchemy)
|   |   |    └── repositories/   # Implementaciones concretas de los puertos (lógica para acceder a los datos). Equivalente a /persistence en NestJS
|   |   ├── dto/                # Para adaptar datos HTTP a entidades o viceversa
|   |   ├── mappers/            # 	Para transformar entre entidades de dominio ↔ modelos ORM ↔ DTOs
│   │   ├── services/ (ej. IA, imágenes)
|   |   ├── scheduler/           # tareas programadas
|   |   ├── auth/                # autenticación (si aplica)
│   ├── interfaces/            # API REST (FastAPI routers) / endpoints REST
|   ├── requirements.txt
|   ├── Dockerfile
│   └── main.py                # Arranque de la app
│
├── frontend/                # Frontend basado en NextJs
|   ├── src/
│   ├── app/
│   │   ├── page.tsx              # página raíz
│   │   └── layout.tsx            # layout global
│   ├── components/
|   ├── services/                 # llamadas a la API
|   ├── Dockerfile
|   ├── Resto de archivos               
├── docker-compose.yml
└── .env
```
## 🧠 Equivalencias con NestJS
| NestJS | FastAPI     |
| :-------- | :------- | 
| `/domain/entities/`      | `/domain/entities/` |
| `/domain/ports/`      | `	/domain/repositories/ (en este caso)` |
| `/infrastructure/persistence/`      | `/infrastructure/db/repositories/` |
| `/infrastructure/controllers/`      | `/interfaces/loquesea.router.py` |
| `/infrastructure/dto/`      | `/infrastructure/dto/` | 
| `/infrastructure/mappers/`      | `/infrastructure/mappers/` | 
| `/infrastructure/services/`      | `/infrastructure/services/` | 
| `/infrastructure/scheduler/`      | `/infrastructure/scheduler/` | 

En NestJS sueles agrupar por dominio funcional, aquí en Python preferimos agrupar por tipo de tecnología dentro de infraestructura, lo que sigue siendo muy limpio y flexible.
- Esta estructura es igual de válida que en NestJS, pero orientada a claridad técnica en vez de modularidad de dominio

## 🧩 Fases del proyecto
### 🟩 Fase 1: Login, registro, panel básico
- Usuarios con login/registro (JWT con `python-jose[cryptography]` y `passlib[bcrypt] + OAuth2`)

- PostgreSQL como base de datos

- Docker Compose con FastAPI + Postgres

- Arquitectura hexagonal base

### 🟨 Fase 2: Subida de imágenes
- Upload de imagen (guardar en local o S3/MinIO)

- Asociación imagen ↔ usuario

- Planteamiento de soft delete (Lo implementaré más tarde seguramente)

### 🟧 Fase 3: Generador de hashtags
- Usa modelo de IA como CLIP de OpenAI o alguna red preentrenada (YOLOv8, torchvision, etc.)

- Puedes convertir imagen en texto y de ahí generar hashtags

- Opcional: entrenar un pequeño modelo si quieres experimentar

### 🟥 Fase 4: Panel admin y dashboard
- Lista de usuarios

- Filtro por fechas, cantidad de imágenes

- Estadísticas simples

# 🚀 Guía de despliegue local - Content Generator API

Esta guía te permitirá clonar y desplegar este proyecto siguiendo arquitectura hexagonal usando Docker y FastAPI.

---
## ⚙️ Pasos para levantar el proyecto

### 1. Clona el repositorio (preferentemente dentro de WSL si usas Windows)

```bash
git clone https://github.com/tu-usuario/fastapi-content-generator.git
cd fastapi-content-generator

```
### 2. Crea el archivo .env
Este archivo contiene las variables sensibles y no está incluido en el repositorio por seguridad.
✅ También puedes usar el archivo .env.example como plantilla, está disponible en el repositorio.

```bash
touch .env
```
Añade el siguiente contenido (ajústalo si es necesario):

```
# PostgreSQL configuration - NO PÚBLICO, ES UN EJEMPLO
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name
POSTGRES_HOST=your_postgres_host
POSTGRES_PORT=5432

# Encriptación de contraseñas y generación de tokens JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

```

### 3. Instala dependencias **(solo si NO usas Docker)**
Si prefieres correr la app **sin** contenedores:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Para **desactivar** el entorno virtual cuando termines de trabajar, simplemente ejecuta:
```bash
deactivate
```

No elimina el entorno ni los paquetes; simplemente deja de estar activo. Cuando quieras volver a usarlo, puedes reactivarlo con:
```bash
source venv/bin/activate
(En Windows: venv\Scripts\activate)
```
---


## ▶️ Levantar el entorno con Docker 
Este proyecto incluye dos contenedores principales:

- 📦 Backend (FastAPI)

- 🖥️ Frontend (NextJs)

Para construir e iniciar todos los servicios:
```
docker-compose up --build
```
Esto iniciará: 
⚙️ FastAPI en → http://localhost:8000

🧩 Frontend en → http://localhost:3000

El contenedor del frontend ejecutará automáticamente **```npm install```** y **```npm run dev```**, así que **no** necesitas hacer nada más desde la terminal.

## 🧪 Endpoints disponibles (API REST)
📍 GET / → http://localhost:8000 - Verifica que la API está corriendo

📄 GET /docs → http://localhost:8000/docs - Documentación interactiva Swagger

📘 GET /redoc → http://localhost:8000/redoc - Documentación ReDoc

## 📌 Notas adicionales
- Si usas Windows, se recomienda trabajar desde **WSL con Ubuntu** para evitar problemas de rutas y permisos.

- También, asegurate de que tener instalado npm y nodejs dentro de WSL, y de tener bien configurado npm para que no esté apuntando a la instalación de Windows.

- Usa `code .` desde tu terminal WSL para abrir Visual Studio Code directamente conectado a tu entorno Linux Ubuntu.

- Asegúrate de que Docker + Docker Compose esté correctamente instalado y corriendo.

- Los contenedores se reiniciarán automáticamente en caso de fallo (restart: on-failure).

- Este proyecto está estructurado para escalar en el futuro.

- La protección de endpoints con acceso habilitado a un usuario loggeado y acceso habilitado a un usuario loggeado + tipo administrador (get_current_user y get_current_admin_user en auth_dependencies.py) en una versión antigua se realizaba con **OAuth2 with Password (and hashing), Bearer with JWT tokens**  [Pincha aquí para saber su funcionamiento](https://github.com/maigcorrea/fastapi-content-generator/blob/main/docs/protección_endpoints_backend_OAuth2(V_antigua).md). Sin embargo, debido al flujo de la aplicación, puesto que el token JWT se genera directamente en el momento de inicio de sesión, se ha decidido actualizar a una nueva versión con Bearer(HTTPBearer) + JWT (Consultar más abajo)

- La protección de rutas desde el Frontend en una versión inicial se comprobaba de forma manual gracias a un contexto y su uso en un componente que envolvía las páginas que componen la aplicación [Pincha aquí para saber su funcionamiento](https://github.com/maigcorrea/fastapi-content-generator/blob/main/docs/protección-rutas-manual(Antigua).md). Pero se ha realizado una actualización con una versión híbrida basada en el encapsulamiento de la lógica de protección en un hook reutilizable + Layout con App Router (Consultar más abajo)

## Detalles relevantes

### **🛡️ Protección de endpoints FastAPI con Bearer + JWT tokens (HTTPBearer)**
La protección de endpoints en una versión antigua se realizaba con **OAuth2 with Password (and hashing), Bearer with JWT tokens**  [Pincha aquí para saber su funcionamiento](https://github.com/maigcorrea/fastapi-content-generator/blob/main/docs/protección_endpoints_backend_OAuth2(V_antigua).md). Sin embargo, debido al flujo de la aplicación, puesto que el token JWT se genera directamente en el momento de inicio de sesión, se ha decidido actualizar a una nueva versión con Bearer(HTTPBearer) + JWT.

El flujo de autenticación está basado en tokens JWT que se envían en la cabecera Authorization usando el esquema Bearer.

- La aplicación FastAPI se encarga tanto de la API como de la autenticación.

- Cada vez que el frontend necesita acceder a un endpoint protegido, debe incluir el token JWT.

🔎 Revisémoslo desde esta perspectiva simplificada:

- El usuario escribe el nombre de usuario y la contraseña en el frontend y pulsa Intro.
- El frontend (que se ejecuta en el navegador del usuario) envía ese nombre de usuario y contraseña al endpoint /users/login de la API.
- La API comprueba ese nombre de usuario y contraseña y responde con un token JWT.
- El frontend almacena ese token JWT temporalmente en algún lugar (localStorage en este caso).
- El usuario hace clic en el frontend para ir a otra sección de la aplicación web frontend.
- El frontend necesita obtener más datos de la API.
- Pero necesita autenticación para ese endpoint específico. Para autenticarse con nuestra API, se envía un encabezado "Autorización" con el valor "Bearer" más el token ```Bearer <token>```.
- Si el token contiene "foobar", el contenido del encabezado "Autorización" sería: "Bearer foobar".

**🔄 Flujo resumido**
El frontend envía usuario/contraseña → obtiene token JWT → lo usa en futuras peticiones.

### 🔐 Flujo de autenticación con HTTPBearer + JWT en FastAPI (implementación real)
**1. Generación del token JWT🔑**

En el endpoint ``` /users/login ``` después de validar las credenciales con ```pwd_context.verify()```, se genera un token JWT que incluye el ```user_id``` como ```sub```:

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
- Extrae el token de la cabecera ```Authorization: Bearer <token>``` con ```HTTPBearer```

- Decodifica el JWT

- Obtiene el user_id del payload (sub)

- Llama al repo para obtener el usuario real (Busca el usuario en la base de datos)

- Lanza un ```error 401``` si algo falla

- Si todo está bien, devuelve el ```current_user```

```python
def get_current_user(token: str = Depends(bearer_scheme), ...):
    ...
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    ...
```

Código completo:
```python
bearer_scheme = HTTPBearer()

def get_current_user(
    credentials = Depends(bearer_scheme),
    user_repo: UserRepository = Depends(get_user_repository)
):
    token = credentials.credentials

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
Gracias a ```HTTPBearer```, FastAPI añade **automáticamente** un botón “Authorize” en la documentación Swagger para probar autenticación con token Bearer.

```python
#En las dependencias
bearer_scheme = HTTPBearer()
```

- Haz clic en "Authorize"

- Introduce el token JWT en el campo

- FastAPI usará el token en los headers automáticamente en los endpoints protegidos

(Adjuntar imagen de swagger)

#### ✅ Resultado
✅ Token seguro con expiración (exp)

✅ Verificación automática en cada endpoint con ```Depends```

✅ Protección opcional para administradores

✅ Integración directa con Swagger y frontend (solo pegar el token)


### **🔐 Sistema de Autenticación y Protección de Rutas (Frontend) con context + hook + Layout**
**⚠️IMPORTANTE:⚠️** La protección de rutas desde el Frontend en una versión anterior se comprobaba de forma manual gracias a un contexto y su uso en un componente que envuelve las páginas que componen la aplicación [Pincha aquí para saber su funcionamiento](https://github.com/maigcorrea/fastapi-hashtag-generator/blob/main/docs/protección-rutas-manual(Antigua).md). Pero se ha realizado una actualización con una versión híbrida basada en el encapsulamiento de la lógica de protección actual en un hook reutilizable + Layout con App Router (Estándar en Nextjs)

#### Arquitectura General
```
<App (Next.js)>
   └── RootLayout (app/layout.tsx)
         └── <AuthProvider> (AuthContext)
               ├── (públicas) login/, permission/, page.tsx
               ├── (private)/layout.tsx  -> usa useAuthGuard(false)
               │       ├── dashboard/page.tsx
               │       └── profile/page.tsx
               └── (admin)/layout.tsx   -> usa useAuthGuard(true)
                       └── admin-panel/page.tsx

```

```mermaid
flowchart TD
  A[Login Form] -->|token & is_admin| B[localStorage]
  B --> C[AuthContext]
  C -->|token/isAdmin| D[Navbar & UI]
  C -->|validación| E[Layouts protegidos]
  E -->|permiso OK| F[Contenido de la ruta]
  E -->|permiso denegado| G['/login o /permission']
```

**1️⃣ Creación del AuthContext**
Se creó un contexto de React (AuthContext) para centralizar el estado de autenticación de la aplicación. Este contexto expone las siguientes propiedades:

- token: token de autenticación del usuario.

- isAdmin: booleano que indica si el usuario es administrador.

- setToken y setIsAdmin: setters para actualizar el estado.

- logout: función que limpia los datos de sesión.

- isLoading: bandera de carga (en la versión final ya no es necesaria, ver optimización).

#### Código base inicial
En la versión inicial, el AuthContext obtenía el token y el rol de localStorage usando un useEffect al montar el componente:

```
useEffect(() => {
  const storedToken = localStorage.getItem("token");
  const storedAdmin = localStorage.getItem("is_admin");

  if (storedToken) setToken(storedToken);
  if (storedAdmin) setIsAdmin(storedAdmin === "true");

  setIsLoading(false);
}, []);

```

**2️⃣ Optimización: inicializar estado desde localStorage**
Para evitar el uso de useEffect y posibles parpadeos al renderizar, se optimizó la inicialización del estado directamente en el useState, leyendo localStorage de manera perezosa (lazy initialization):

```
const [isAdmin, setIsAdmin] = useState<boolean | null>(() => {
  const storedAdmin = localStorage.getItem("is_admin");
  return storedAdmin ? storedAdmin === "true" : null;
});

const [token, setToken] = useState<string>(() => {
  return localStorage.getItem("token") || "";
});
```
Con esto, el contexto ya tiene los valores cargados al momento de inicializarse, e isLoading se vuelve opcional.

**3️⃣ Listener de localStorage para sincronización entre pestañas**
Se añadió un listener de eventos storage para detectar cambios en el localStorage hechos desde otras pestañas o ventanas del navegador. Esto permite que el estado de autenticación se sincronice en tiempo real:
```
useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      // Si se cambió el token o is_admin en otra pestaña, actualizamos el contexto
      if (e.key === "token") {
        setToken(e.newValue || "");
      }
      // Si se cambió is_admin en otra pestaña, actualizamos el contexto
      if (e.key === "is_admin") {
        setIsAdmin(e.newValue ? e.newValue === "true" : null);
      }
      // Si se borró el localStorage completo (logout)
      if (e.key === null) {
        setToken("");
        setIsAdmin(null);
      }
    };

    // Añadimos el listener al evento de storage para detectar cambios en localStorage
    window.addEventListener("storage", handleStorageChange);
    // Limpiamos el listener al desmontar el componente
    // Esto es importante para evitar fugas de memoria y comportamientos inesperados
    return () => window.removeEventListener("storage", handleStorageChange);
  }, []);
```

**4️⃣ Actualización del contexto en ciertas partes de la aplicación, por ej el login**
En el formulario de login, al autenticarse correctamente, se guardan los datos en localStorage y se actualiza el contexto para que el resto de la aplicación pueda reaccionar en tiempo real (por ejemplo, mostrar el Navbar con el usuario logueado):

```
localStorage.setItem("token", data.access_token);
localStorage.setItem("is_admin", String(data.is_admin));

// Actualizar contexto
setToken(data.access_token);
setIsAdmin(data.is_admin);
```
Esto permite que, al hacer login, las rutas protegidas se desbloqueen sin necesidad de recargar la página.

**5️⃣ Hook useAuthGuard**
Centralizamos la lógica de protección en un hook reutilizable:
```ts
'use client';

import { useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { AuthContext } from '@/context/AuthContext';

export function useAuthGuard(adminOnly = false) {
  const { token, isAdmin, isLoading } = useContext(AuthContext);
  const router = useRouter();
  const [authorized, setAuthorized] = useState(false);

  useEffect(() => {
    // Si todavía se está cargando el contexto, no hacemos nada
    if (isLoading) return;

    // Si no hay token -> login
    if (!token) {
      router.push('/login');
      return;
    }

    // Si la ruta requiere admin y el usuario no lo es -> acceso denegado
    if (adminOnly && !isAdmin) {
      router.push('/permission');
      return;
    }

    // Si todo OK -> autorizado
    setAuthorized(true);
  }, [token, isAdmin, isLoading, adminOnly, router]);

  return { authorized, isLoading };
}

```
#### Ventajas del hook:
- Se puede usar tanto en Layouts como en componentes concretos (ej: un botón o sección de UI).

- Toda la lógica de redirección y validación está centralizada.

- Si quieres proteger un componente dentro de una página, puedes usar directamente el hook:
```
const { authorized } = useAuthGuard(true); // solo admins

if (!authorized) return null;

return <button>Eliminar usuarios</button>;

```

**6️⃣ Implementación con Layouts protegidos (Next.js App Router)**
En vez de envolver cada página con <ProtectRoutes>, ahora protegemos grupos de rutas con layouts.

#### Estructura general
```
app/
├─ layout.tsx                 Layout global de toda la app
├─ page.tsx                   Página pública (ej: Home)
│
├─ login/
│   └─ page.tsx               Página pública de login
│
├─ permission/
│   └─ page.tsx               Página de "Acceso denegado"
│
├─ (private)/                 Grupo de rutas privadas (cualquier usuario logueado)
│   ├─ layout.tsx             Layout con useAuthGuard(false)
│   ├─ dashboard/
│   │   └─ page.tsx           Panel privado (cualquier usuario)
│   ├─ profile/
│   │   └─ page.tsx           Perfil del usuario
│   └─ tasks/
│       └─ page.tsx           Otra ruta privada
│
├─ (admin)/                   Grupo de rutas solo para admins
│   ├─ layout.tsx             Layout con useAuthGuard(true)
│   └─ admin-panel/
│       └─ page.tsx           Panel exclusivo de admins

```
#### ¿Cómo funcionan los grupos (private) y (admin)?
- (private)
  - Todas las páginas dentro de esa carpeta comparten el layout.tsx de (private)
  - Ese layout usa useAuthGuard(false) → solo requiere que el usuario esté logueado.


- (admin)
  - Todas las páginas dentro de esa carpeta comparten el layout.tsx de (admin)
  - Ese layout usa useAuthGuard(true) → requiere ser admin

#### Flujo de validación de los layouts
```mermaid
flowchart TD
  A[Token existe?] -->|NO| B[redirige /login]
  A -->|SÍ| C[¿adminOnly?]
  C -->|NO| D[Renderiza children]
  C -->|SÍ| E[isAdmin true?]
  E -->|NO| F[redirige /permission]
  E -->|SÍ| D[Renderiza children]

```

*Layout para rutas privadas:*
```tsx
'use client';

import { ReactNode } from 'react';
import { useAuthGuard } from '@/hooks/useAuthGuard';

export default function PrivateLayout({ children }: { children: ReactNode }) {
  const { authorized, isLoading } = useAuthGuard(false); // false = cualquier usuario logueado

  if (isLoading || !authorized) return null;

  return <>{children}</>;
}

```

*Layout para rutas a las que sólo el admin puede acceder:*
```tsx
'use client';

import { ReactNode } from 'react';
import { useAuthGuard } from '@/hooks/useAuthGuard';

export default function AdminLayout({ children }: { children: ReactNode }) {
  const { authorized, isLoading } = useAuthGuard(true); // true = solo admins

  if (isLoading || !authorized) return null;

  return <>{children}</>;
}

```
#### ¿Qué se consigue?
- Todas las páginas dentro de (private) requieren estar logueado.

- Todas las páginas dentro de (admin) requieren además ser admin.

- Ya no hay que envolver nada manualmente, el layout se aplica automáticamente.


#### FLUJOS DE NAVEGACIÓN

##### Flujo completo (Login -> Rutas protegidas -> logout)
```mermaid
sequenceDiagram
  participant User
  participant LoginForm
  participant AuthContext
  participant useAuthGuard
  participant Layouts

  User->>LoginForm: Ingresa credenciales
  LoginForm->>localStorage: Guarda token & is_admin
  LoginForm->>AuthContext: setToken() & setIsAdmin()
  AuthContext->>Layouts: Contexto actualizado
  Layouts->>useAuthGuard: Verifica permisos
  useAuthGuard->>Layouts: Permiso OK o redirección
  Layouts->>UI: Renderiza children permitidos
  User->>AuthContext: logout()
  AuthContext->>localStorage: clear()
  Layouts->>useAuthGuard: Revalida -> redirige a login

```
```mermaid
flowchart TD
    A[Usuario entra a /dashboard] --> B{token existe?}
    B -- No --> C[Redirigir a /login]
    C --> D[Usuario hace login]
    D --> E[Guardar token e isAdmin en AuthContext y localStorage]
    E --> F[Usuario navega a /dashboard]
    F --> G{token existe?}
    G -- Sí --> H[Renderizar Dashboard]

    H --> I[Usuario navega a /admin-panel]
    I --> J{isAdmin = true?}
    J -- No --> K[Redirigir a /permission]
    J -- Sí --> L[Renderizar Admin Panel]

    L --> M[Usuario hace logout]
    M --> N[Limpiar AuthContext y localStorage]
    N --> C

```
- No hay que poner lógica en cada página.
- Todo depende de ```token``` e ```isAdmin``` en el ```AuthContext```.




#### Beneficios de esta implementación
- Centralización del estado de autenticación en un solo lugar (```AuthContext```).

- Sincronización multi-pestaña: login y logout se propagan en tiempo real.

- Sin parpadeos: al inicializar el contexto directamente desde localStorage, evitamos renderizados intermedios incorrectos.

- Protección de grupos completos de rutas con los Layouts del App Router. 

- Se siguen podiendo proteger componentes individuales gracias al hook useAuthGuard.

- UI se actualiza automáticamente al login/logout.


### **Esquema de flujo de subida, obtención de URLs firmadas y renderizado de imagenes (backend+frontend)**

```mermaid
sequenceDiagram
    participant F as Frontend (Next.js)
    participant B as Backend (FastAPI)
    participant S3 as MinIO / AWS S3

    Note over F B S3: Subida de imagen
    F->>B: POST /images/upload (archivo + JWT)
    B->>S3: Subir archivo al bucket privado
    B->>B: Guardar file_name en la BD
    B-->>F: OK (datos de la imagen)

    Note over F B S3: Visualización de imagen
    F->>B: GET /images/me (JWT)
    B-->>F: Lista de imágenes (file_name)
    F->>B: GET /images/image-url/{id} (JWT)
    B->>S3: Generar URL firmada
    S3-->>B: URL firmada
    B-->>F: URL firmada (localhost:9000 o amazonaws.com)
    F->>S3: Solicitar imagen con la URL firmada
    S3-->>F: Imagen
```

- [Subida de imagenes a MinIO con estructura compatible para S3](https://github.com/maigcorrea/fastapi-content-generator/blob/main/docs/subida_img_s3.md)

- [Gestión de imagenes privadas con URLs firmadas (Presigned URLs for private buckets)](https://github.com/maigcorrea/fastapi-content-generator/blob/main/docs/gestión_img_privadas_url_firmadas.md)


### **🗑 Gestión de imágenes con Soft Delete, Papelera, Restauración y Cron Job**
Este módulo extiende el sistema de imágenes (MinIO/AWS S3 + URLs firmadas) añadiendo:

1. Eliminación lógica (soft delete): las imágenes no se eliminan inmediatamente, sino que se marcan como borradas (is_deleted = True).

2. Papelera (trash): los usuarios pueden ver y restaurar imágenes borradas antes de que se eliminen definitivamente.

3. Cron Job: Se ejecuta cada medianoche y elimina definitivamente las imágenes marcadas como borradas hace más de 30 días (de la base de datos y del bucket S3/MinIO).

#### Flujo final de gestión de imágenes
**1. El usuario sube una imagen**

  - Se guarda en MinIO (bucket privado).

  - Se guarda el registro en BD (con ```deleted_at = NULL y is_deleted = false```).


**2. El usuario puede ver su historial de imágenes**

  - Solo se listan imágenes is_deleted = false.


**3. Si el usuario elimina una imagen**

  - Se marca como is_deleted = true y se setea deleted_at = NOW().

  - La imagen ya no aparece en el historial.

  - La imagen sigue estando en MinIO por si el usuario la quiere restaurar.


**4. El usuario puede restaurar imágenes borradas**

  - Si ```NOW() - deleted_at < X días```, puede restaurar (is_deleted = false y deleted_at = NULL).


  - Si ha pasado el tiempo, ya no se podrá restaurar (porque el cron la habrá eliminado).


**5. Tarea cron (cada día de madrugada)**

  - Busca imágenes con ```is_deleted = true``` y ```deleted_at < NOW() - X días```.


  - Borra el archivo en MinIO (s3_client.delete_object) y borra el registro en la BD.


- [Ver documentación completa acerca de la gestión de eliminación imagenes mediante soft delete, papelera, restauración de img y cron](https://github.com/maigcorrea/fastapi-content-generator/blob/main/docs/gestión_eliminación_img.md)




## Autores
- [@maigcorrea](https://www.github.com/maigcorrea)

- © 2025 Ana Maite García Correa. Todos los derechos reservados.
No se permite el uso, copia, modificación o distribución de este software sin permiso explícito por escrito al correo anamaitegarciacorrea@gmail.com.

