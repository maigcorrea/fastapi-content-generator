# HastagsGenerator

Este proyecto es una API de generación de hashtags a partir de imágenes, construida con **FastAPI**, **PostgreSQL**, **Docker** y con estructura de **arquitectura hexagonal (Clean Architecture)**.
Proyecto para aprender Python orientado a IA + web + arquitectura limpia

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


## 🧠 Tecnologías sugeridas por capa
| Capa | Tecnología     |
| :-------- | :------- | 
| `Interfaz`      | `FastAPI (backend API REST) + React (opcional)` |
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
- Usuarios con login/registro (JWT)

- PostgreSQL como base de datos

- Docker Compose con FastAPI + Postgres

- Arquitectura hexagonal base

### 🟨 Fase 2: Subida de imágenes
- Upload de imagen (guardar en local o S3/MinIO)

- Asociación imagen ↔ usuario

### 🟧 Fase 3: Generador de hashtags
- Usa modelo de IA como CLIP de OpenAI o alguna red preentrenada (YOLOv8, torchvision, etc.)

- Puedes convertir imagen en texto y de ahí generar hashtags

- Opcional: entrenar un pequeño modelo si quieres experimentar

### 🟥 Fase 4: Panel admin y dashboard
- Lista de usuarios

- Filtro por fechas, cantidad de imágenes

- Estadísticas simples

# 🚀 Guía de despliegue local - Hashtag Generator API

Esta guía te permitirá clonar y desplegar este proyecto siguiendo arquitectura hexagonal usando Docker y FastAPI.

---
## ⚙️ Pasos para levantar el proyecto

### 1. Clona el repositorio (preferentemente dentro de WSL si usas Windows)

```bash
git clone https://github.com/tu-usuario/hashtag-generator.git
cd hashtag-generator

```
### 2. Crea el archivo .env
Este archivo contiene las variables sensibles y no está incluido en el repositorio por seguridad.
✅ También puedes usar un archivo .env.example como plantilla, está disponible en el repositorio.

```bash
touch .env
```
Añade el siguiente contenido (ajústalo si es necesario):

```
# PostgreSQL configuration - NO PÚBLICO, ES UN EJEMPLO
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name

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

El contenedor del frontend ejecutará automáticamente npm install y npm run dev, así que no necesitas hacer nada más desde la terminal.

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

## Autores
- [@maigcorrea](https://www.github.com/maigcorrea)

- © 2025 Ana Maite García Correa. Todos los derechos reservados.
No se permite el uso, copia, modificación o distribución de este software sin permiso explícito por escrito.

