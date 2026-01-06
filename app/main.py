from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from .database import engine, Base
from .routers import auth, chat

# 1. Create Database Tables
# This creates the file 'tutor.db' if it doesn't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="O/A Level AI Tutor")

# 2. Connect the Routers
app.include_router(auth.router)
app.include_router(chat.router)

# 3. Mount Static Files (The Frontend)
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Check if static directory exists to prevent startup errors
if not STATIC_DIR.exists():
    # Only for first run/setup purposes
    import os
    os.makedirs(STATIC_DIR)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# 4. Serve the Home Page
@app.get("/")
def read_root():
    return FileResponse(STATIC_DIR / "index.html")