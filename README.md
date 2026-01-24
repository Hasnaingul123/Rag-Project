# 🎓 AI Tutor (RAG-Based Learning Assistant)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-green)
![LangChain](https://img.shields.io/badge/LangChain-v0.1-orange)
![Llama 3](https://img.shields.io/badge/AI-Meta--Llama--3--8B-purple)

**AI Tutor** is a Full-Stack Retrieval-Augmented Generation (RAG) application designed to help O/A Level students study efficiently. Users can upload their study notes (PDFs), and the AI acts as a personalized tutor, answering questions strictly based on the uploaded material to ensure accuracy and prevent hallucinations.

---

## 🚀 Key Features

-   **📚 Document Ingestion:** Upload PDF study materials, which are chunked, embedded, and stored in a vector database.
-   **🧠 Context-Aware Answers:** Uses **Meta-Llama-3-8B-Instruct** to generate answers based *only* on your uploaded documents.
-   **🔐 User Authentication:** Secure Signup/Login system using **JWT (JSON Web Tokens)** and **BCrypt** password hashing.
-   **🧹 Dynamic Memory Management:** Includes a "Reset Memory" feature to clear the database and switch subjects instantly without context overlap.
-   **⚡ Fast Retrieval:** Uses **ChromaDB** and **all-MiniLM-L6-v2** embeddings for sub-second information retrieval.

---

## 🛠️ Tech Stack

### **Backend**
-   **Framework:** FastAPI (Python)
-   **AI Orchestration:** LangChain
-   **LLM Provider:** Hugging Face Inference API
-   **Vector Database:** ChromaDB
-   **Relational Database:** SQLite (for User Data)

### **Frontend**
-   **Core:** HTML5, CSS3, Vanilla JavaScript
-   **Interaction:** Fetch API for asynchronous communication with the backend.

### **AI Models**
-   **Generator:** `meta-llama/Meta-Llama-3-8B-Instruct`
-   **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`

---

## 📂 Project Structure

```text
rag-tutor/
├── app/
│   ├── routers/        # API Routes (Auth, Chat)
│   ├── static/         # Frontend Files (HTML, CSS, JS)
│   ├── crud.py         # Database Operations (Create, Read, Update, Delete)
│   ├── database.py     # SQLite Connection
│   ├── main.py         # Application Entry Point
│   ├── models.py       # SQLAlchemy Database Models
│   ├── rag.py          # RAG Logic (Ingestion & Retrieval Pipeline)
│   ├── schemas.py      # Pydantic Data Validation Schemas
│   └── utils.py        # Password Hashing Utilities
├── data/               # Temp storage for uploaded PDFs

⚡ Installation & Setup
Follow these steps to run the project locally.

1. Clone the Repository
Bash
git clone [https://github.com/Hasnaingul123/Rag-Project.git](https://github.com/Hasnaingul123/Rag-Project.git)
cd Rag-Project
2. Create a Virtual Environment
Bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the root directory and add your keys:

Code snippet
HF_TOKEN=your_huggingface_api_token_here
SECRET_KEY=your_random_secret_string_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
(Note: You can get a free token from Hugging Face)

5. Run the Server
Bash
uvicorn app.main:app --reload
The application will be live at: https://www.google.com/search?q=http://127.0.0.1:8000

📖 How to Use
Sign Up/Login: Create an account to access the dashboard.

Upload PDF: Click the "Upload" button to feed your notes to the AI.

Ask Questions: Type questions like "Explain the concept of osmosis based on the document."

Reset: Switching subjects? Click "Clear Memory" to wipe the brain and start fresh with a new document.

🔮 Future Roadmap
[ ] Deploy to Cloud (Render/AWS).

[ ] Add support for multiple documents at once.

[ ] Implement "Conversation History" (Chat Memory).

[ ] Add Citation (Page numbers) to answers.

🤝 Contributing
Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

Built with ❤️ by Hasnain Gul
├── chroma_db/          # Vector Database Storage
├── requirements.txt    # Project Dependencies
└── README.md           # Project Documentation
