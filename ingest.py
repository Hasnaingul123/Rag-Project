import os
import shutil
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. Configuration
PDF_PATH = "data/sample_textbook.pdf"
CHROMA_PATH = "chroma_db"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

def main():
    # --- Step 1: Load ---
    if not os.path.exists(PDF_PATH):
        print(f"❌ Error: File {PDF_PATH} not found.")
        print("Please place a PDF file named 'sample_textbook.pdf' in the 'data' folder.")
        return

    print("📚 Loading PDF...")
    loader = PyPDFLoader(PDF_PATH)
    raw_documents = loader.load()

    # --- Step 2: Split ---
    print("✂️ Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(raw_documents)
    print(f"✅ Created {len(chunks)} chunks.")

    # --- Step 3: Embed & Store ---
    print("💾 Saving to Vector Database (This uses local HF Embeddings)...")
    
    # Clear existing DB to avoid duplicates during testing
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Initialize the Hugging Face Embedding function
    embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    # Create the Chroma Database
    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=CHROMA_PATH
    )

    print(f"🚀 Success! {len(chunks)} chunks saved to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()