from fastapi import FastAPI
from app.infrastructure.db.db_config import Base, engine
from app.infrastructure.db.models.user_model import UserModel # Import the UserModel to ensure it's registered with SQLAlchemy
from app.interfaces import user_router  # importa el router

app = FastAPI(title="Hashtag Generator API")

@app.on_event("startup")
def startup():
    print("🔌 Connecting to the database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database ready.")

app.include_router(user_router.router)  # registra el router

@app.get("/")
def read_root():
    return {"message": "Hashtag Generator API is running 🚀"}