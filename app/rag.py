import os
import shutil
from dotenv import load_dotenv

load_dotenv()

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Configuration
CHROMA_PATH = "chroma_db"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

# 2. Setup LLM (Hugging Face)
# We use the 8B model for maximum reliability on the free tier.
# If you have a Pro account, you can switch back to "meta-llama/Llama-3.1-70B-Instruct"
REPO_ID = "meta-llama/Meta-Llama-3-8B-Instruct"

# Step A: Create the Base Endpoint
# We remove the explicit 'task' parameter to let HF auto-negotiate the best task
llm_engine = HuggingFaceEndpoint(
    repo_id=REPO_ID,
    huggingfacehub_api_token=os.getenv("HF_TOKEN"),
    temperature=0.3,
    max_new_tokens=1024,
    do_sample=True,
)

# Step B: Wrap it in ChatHuggingFace
# This correctly formats messages (System/Human) for the model, preventing "Conversational" errors
llm = ChatHuggingFace(llm=llm_engine)

# 3. The "O/A Level" Persona
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are an expert O/A Level Tutor. Your goal is to help students prepare for their exams (IGCSE/GCE).
    
    Rules:
    1. Answer ONLY based on the context provided (the uploaded PDF).
    2. Explain concepts simply and clearly, suitable for a 16-18 year old student.
    3. If the context contains definitions or formulas, highlight them.
    4. If the answer is not in the context, say: "I cannot find this information in the uploaded notes."
    """),
    ("human", "Context: {context}\n\nQuestion: {question}")
])

def get_vector_db():
    """Helper to get the current database connection."""
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function
    )

# 4. The Ingestion Function
def process_pdf(file_path: str):
    print("🔄 Processing new PDF...")
    
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(docs)
    
    new_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=CHROMA_PATH
    )
    print("✅ New PDF Ingested Successfully!")
    return True

# 5. The Retrieval Chain
def ask_question(query: str):
    vector_db = get_vector_db()
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )
    
    try:
        answer = rag_chain.invoke(query)
        # Clean up any potential whitespace issues
        return {"answer": answer.strip()}
    except Exception as e:
        print(f"RAG Error: {e}")
        return {"answer": f"I encountered an error connecting to the model: {str(e)}"}