from fastapi import FastAPI
from app.infrastructure.db.db_config import Base, engine

app = FastAPI(title="Hashtag Generator API")

@app.on_event("startup")
def startup():
    print("🔌 Connecting to the database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database ready.")

@app.get("/")
def read_root():
    return {"message": "Hashtag Generator API is running 🚀"}