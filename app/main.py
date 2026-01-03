from fastapi import FastAPI
from .database import engine, Base
from . import models

# This line commands the engine to look at our 'models' and create the tables 
# in the database if they don't exist yet.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG Tutor API"}