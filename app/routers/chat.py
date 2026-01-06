import os
import shutil
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from .. import rag

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
def query_tutor(request: QueryRequest):
    """
    Endpoint to ask the AI Tutor a question based on ingested data.
    """
    return rag.ask_question(request.query)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Receives a PDF file, saves it, and feeds it to the AI.
    """
    try:
        # Ensure data folder exists
        os.makedirs("data", exist_ok=True)
        
        # 1. Define where to save the temp file
        file_location = os.path.join("data", file.filename)
        
        # 2. Save the file locally
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
            
        # 3. Trigger the Brain to learn this file
        rag.process_pdf(file_location)
        
        return {"message": "Knowledge base updated successfully! I am ready to answer questions."}
        
    except Exception as e:
        print(f"Upload Error: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")