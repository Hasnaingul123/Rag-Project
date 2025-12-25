# Project Specifications: Intelligent RAG-Based Educational Tutor

## 1. Executive Summary
This project aims to build a full-stack educational web application where students can register, enroll in O-Level/A-Level courses (Physics, Chemistry, Computer Science), and interact with an AI tutor. The AI tutor uses **Retrieval Augmented Generation (RAG)** to provide accurate answers sourced strictly from the course textbooks.

## 2. Technical Architecture

### 2.1 Technology Stack
- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **LLM Orchestration**: [LangChain](https://python.langchain.com/)
- **Vector Database**: [ChromaDB](https://www.trychroma.com/) (for storing textbook embeddings)
- **Relational Database**: SQLite (for user, course, and enrollment data)
- **ORM**: SQLAlchemy or SQLModel
- **Authentication**: OAuth2 with JWT (JSON Web Tokens)
- **Frontend**: Clean HTML/CSS/JavaScript (or extensive framework if preferred, but keep it simple initially)

### 2.2 System Architecture
1.  **Ingestion Service**: Processes PDF textbooks, chunks text, generates embeddings, and stores them in ChromaDB.
2.  **Auth Service**: Handles user signup, login, and token generation.
3.  **Application Logic**: API endpoints to manage courses and handle chat interactions.
4.  **RAG Engine**: 
    -   Receives user query.
    -   Retrieves relevant context from ChromaDB.
    -   Passes Query + Context to LLM via LangChain.
    -   Returns answer to user.

## 3. Database Schema (SQLite)

### 3.1 Users Table
- `id`: Integer, Primary Key
- `username`: String, Unique
- `email`: String, Unique
- `hashed_password`: String
- `role`: Enum (student, admin) - *Optional for now*
- `created_at`: Datetime

### 3.2 Courses Table
- `id`: Integer, Primary Key
- `title`: String (e.g., "O-Level Physics")
- `description`: String
- `collection_name`: String (The internal name used in ChromaDB for this book)

### 3.3 Enrollments Table
- `id`: Integer, Primary Key
- `user_id`: ForeignKey(Users.id)
- `course_id`: ForeignKey(Courses.id)
- `enrolled_at`: Datetime

### 3.4 ChatHistory (Optional for MVP)
- `id`: Integer
- `user_id`: ForeignKey
- `message`: Text
- `response`: Text
- `timestamp`: Datetime

## 4. API Endpoints Specification

### 4.1 Authentication (`/auth`)
- `POST /auth/signup`: Create a new user account.
- `POST /auth/login`: Authenticate and return Access Token.

### 4.2 Courses (`/courses`)
- `GET /courses/`: List all available courses.
- `POST /courses/{course_id}/enroll`: Enroll the current user in a course.

### 4.3 Chat (`/chat`)
- `POST /chat/query`: 
    -   **Input**: `{ "course_id": 1, "query": "What is Newton's Second Law?" }`
    -   **Logic**: 
        1. Verify user is enrolled in `course_id`.
        2. Fetch `collection_name` for the course.
        3. Perform RAG search in ChromaDB.
        4. Generate response using LLM.
    -   **Output**: `{ "answer": "...", "sources": [...] }`

## 5. RAG Implementation Guidelines

### 5.1 Data Ingestion Script (`ingest.py`)
You must create a standalone script to populate the vector database.
1.  **Load**: Use `PyPDFLoader` (from `langchain_community.document_loaders`) to read the textbook PDFs.
2.  **Split**: Use `RecursiveCharacterTextSplitter` to chunk data (e.g., chunk_size=1000, overlap=200).
3.  **Embed**: Use a standard embedding model (e.g., OpenAIEmbeddings or HuggingFaceEmbeddings).
4.  **Store**: Persist chunks into ChromaDB, using a separate collection for each subject (e.g., `physics_collection`, `chemistry_collection`).

### 5.2 Retrieval Chain
Use LangChain's `RetrievalQA` or `create_retrieval_chain`.
-   **Prompt Template**: Ensure the system prompt instructs the LLM to *only* answer based on the provided context.
    > "You are a helpful tutor. Answer the question based only on the following context: {context}"

## 6. Frontend Specifications
-   **Login/Signup Page**: Simple forms to get JWT token.
-   **Dashboard**: List available courses with an "Enroll" button.
-   **Chat Interface**:
    -   Dropdown to select an active course.
    -   Chat window (User message bubble, AI response bubble).
    -   Loading state while fetching answer.

## 7. Development Roadmap

### Phase 1: Setup & Auth
-   Initialize FastAPI project structure.
-   Set up SQLite database and SQLAlchemy models.
-   Implement Signup/Login with JWT.

### Phase 2: RAG Backend
-   Set up ChromaDB locally.
-   Write `ingest.py` to index a sample PDF.
-   Create a basic endpoint to test retrieval (without LLM first, just check if correct chunks are found).

### Phase 3: The Full Chain
-   Integrate LangChain.
-   Connect the Chat endpoint to the RAG chain.
-   Ensure answers are context-aware.

### Phase 4: Frontend & Polish
-   Build the UI.
-   Connect UI to APIs.
-   Test with real O-Level questions.

## 8. Requirements for the Intern
-   **Code Quality**: Use Type hints (Pydantic models) everywhere.
-   **Documentation**: Comment your functions.
-   **Env Vars**: Store API keys (OpenAI/HuggingFace) in a `.env` file. DO NOT hardcode them.

## 9. Git & GitHub Workflow Guideness
As a professional engineer, following a strict version control workflow is mandatory.

### 9.1 Branching Strategy
-   **`main`**: This branch is for production-ready code ONLY. Do not push directly to `main`.
-   **`develop`**: This is your primary working branch. All new features and fixes should be merged here first.
-   **Feature Branches**: When working on a specific task (e.g., "setup-auth" or "create-rag-pipeline"), create a new branch from `develop`.
    -   Naming convention: `feature/feature-name` or `fix/issue-description`.

### 9.2 Commit Messages
Write clear, descriptive commit messages.
-   **Bad**: "fixed bug", "wip", "update"
-   **Good**: "feat: implement JWT authentication logic", "fix: resolve ChromaDB connection error", "docs: update API documentation"
-   Use conventional commits if possible (feat, fix, docs, style, refactor).

### 9.3 Pull Requests (PR)
When a feature is complete:
1.  Push your feature branch or changes to the remote repository.
2.  Create a **Pull Request (PR)** targeting the `main` branch (or `develop` first if we are doing strict git-flow, but for now targeting `main` from your final `develop` state is acceptable for review).
3.  **Review**: I (the Senior Engineer) will review your PR.
    -   I will check for code quality, strict typing, and adherence to specs.
    -   If changes are requested, apply them and push again to update the PR.
4.  Once approved, I will squash and merge your code into `main`.

**Important**: Never force push to shared branches unless explicitly told to do so.
