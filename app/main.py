from fastapi import FastAPI
from .database import engine
from . import models
from .routers import auth # Import the new router

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Connect the auth router to the main app
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG Tutor API"}