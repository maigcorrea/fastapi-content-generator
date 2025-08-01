from fastapi import FastAPI
from infrastructure.db.db_config import Base, engine
from fastapi.middleware.cors import CORSMiddleware # Import CORS middleware
from infrastructure.db.models.user_model import UserModel # Import the UserModel to ensure it's registered with SQLAlchemy
from infrastructure.db.models.image_model import ImageModel  # Import the ImageModel to ensure it's registered with SQLAlchemy
from infrastructure.db.models.pending_user_model import PendingUser  # Import the PendingUser to ensure it's registered with SQLAlchemy
from interfaces import user_router  # importa el router
from interfaces import image_router  # importa el router de imágenes
from fastapi.staticfiles import StaticFiles

# Registrar el cron
# from apscheduler.schedulers.background import BackgroundScheduler
# from infrastructure.scheduler.delete_old_images import delete_old_images
from infrastructure.scheduler.scheduler import start_scheduler, stop_scheduler # Importa el scheduler centralizado

# AHORA ESTO SE HACE DESDE scheduler.py 
# Configurar el cron para eliminar imágenes antiguas (Antes de crear la instancia de FastAPI, esto asegura que el cron se inicie junto al arrancar la aplicación)
# Sólo si se inicializa, se arranca en el evento startup
# scheduler = BackgroundScheduler()
# scheduler.add_job(delete_old_images, "cron", hour=0, minute=0)


app = FastAPI(title="Hashtag Generator API")

@app.on_event("startup")
def startup():
    print("🔌 Connecting to the database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database ready.")

    # Iniciar scheduler (con todos los cron jobs) aquí evita duplicados en desarrollo con --reload
    start_scheduler()

# Apagar scheduler al cerrar la aplicación
@app.on_event("shutdown")
def shutdown_event():
    stop_scheduler()

# Montar la carpeta estática para servir imágenes (Ya no es necesario, ya que las imágenes se sirven desde MinIO/S3)
#app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

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

