from fastapi import FastAPI

app = FastAPI(title="Hashtag Generator API")

@app.get("/")
def read_root():
    return {"message": "Hashtag Generator API is running 🚀"}