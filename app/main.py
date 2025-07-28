from fastapi import FastAPI
from infrastructure.db.db_config import Base, engine
from fastapi.middleware.cors import CORSMiddleware # Import CORS middleware
from infrastructure.db.models.user_model import UserModel # Import the UserModel to ensure it's registered with SQLAlchemy
from infrastructure.db.models.image_model import ImageModel  # Import the ImageModel to ensure it's registered with SQLAlchemy
from interfaces import user_router  # importa el router
from interfaces import image_router  # importa el router de imágenes
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Hashtag Generator API")

@app.on_event("startup")
def startup():
    print("🔌 Connecting to the database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database ready.")

# Montar la carpeta estática para servir imágenes
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Registrar los routers
app.include_router(user_router.router)  # registra el router
app.include_router(image_router.router)  # registra el router de imágenes


# CORS settings

origins = [
    "http://localhost:3000",
    "http://frontend:3000",  # para acceso dentro de docker
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # o ["*"] para todos (solo en desarrollo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hashtag Generator API is running 🚀"}