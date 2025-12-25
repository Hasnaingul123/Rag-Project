from fastapi import FastAPI
from .auth.routes import router as auth_router

app = FastAPI(title="RAG Tutor API")

app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "RAG Tutor Running 🚀"}
