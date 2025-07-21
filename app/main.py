from fastapi import FastAPI
from app.infrastructure.db.db_config import Base, engine
from fastapi.middleware.cors import CORSMiddleware # Import CORS middleware
from app.infrastructure.db.models.user_model import UserModel # Import the UserModel to ensure it's registered with SQLAlchemy
from app.interfaces import user_router  # importa el router

app = FastAPI(title="Hashtag Generator API")

@app.on_event("startup")
def startup():
    print("🔌 Connecting to the database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database ready.")

app.include_router(user_router.router)  # registra el router


# CORS settings
origins = [
    origins = [
    "http://localhost:5173",
    "http://frontend:5173",  # para acceso dentro de docker
]
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