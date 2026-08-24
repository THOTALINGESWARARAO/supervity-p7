HR Knowledge Assistant

A full-stack, RAG-powered HR Knowledge Assistant combining semantic
document retrieval, LLM-based question answering, agent capabilities,
conversation memory, task management, and a React frontend.

Table of Contents

Project Overview

Objectives

Key Features

System Architecture

Request Flow

Technology Stack

Project Structure

HR Knowledge Base

RAG Pipeline

Agent Layer

Conversation Memory

Task Management

FastAPI API

React Frontend

Environment Configuration

Local Installation

Running the Application

API Examples

Testing and Validation

Task 10 Full Integration

Production Build

Deployment Status

Deployment Considerations

Security

Troubleshooting

Development Workflow

Project Status

Repository

Project Overview

P7 is a full-stack AI application designed to provide an internal HR
knowledge assistant.

Instead of relying only on an LLM's general knowledge, the system
retrieves relevant information from a controlled HR document collection
and uses that context to generate answers.

The project also extends beyond basic RAG by integrating:

An HR-focused agent

Conversation memory

Task management

REST APIs

A React user interface

Automated testing

End-to-end local integration validation

The resulting system can be viewed as:

                ┌──────────────────────┐
                │    React Frontend    │
                │       Vite + React   │
                └──────────┬───────────┘
                           │
                           │ HTTP / JSON
                           ▼
                ┌──────────────────────┐
                │     FastAPI API      │
                │                      │
                │ /ask   /agent        │
                │ /tasks /health       │
                └───────┬───────┬──────┘
                        │       │
              ┌─────────┘       └────────────┐
              ▼                              ▼
       ┌───────────────┐              ┌───────────────┐
       │ RAG Pipeline  │              │ Agent / Tools │
       └───────┬───────┘              └───────┬───────┘
               │                              │
       ┌───────▼────────┐             ┌───────▼────────┐
       │ FAISS Vector   │             │ Task Management│
       │ Store          │             │ + Memory       │
       └───────┬────────┘             └────────────────┘
               │
       ┌───────▼────────┐
       │ HR Documents   │
       │ + Embeddings   │
       └───────┬────────┘
               │
               ▼
       ┌────────────────┐
       │ Groq LLM       │
       └────────────────┘

Objectives

The project was developed to demonstrate practical AI engineering rather
than a standalone model call.

The main objectives are:

Build a document-grounded HR question-answering system.

Implement semantic retrieval with embeddings and FAISS.

Connect retrieval results to an LLM for grounded generation.

Provide an agent interface for natural-language requests.

Add conversation memory for multi-turn interactions.

Implement task creation and lifecycle management.

Expose functionality through a FastAPI backend.

Build a React frontend consuming the backend API.

Validate the system through automated tests.

Perform full local integration testing before deployment.

Key Features

1. HR Knowledge Retrieval

Users can ask questions about internal HR information.

Example:

What is the company's leave policy?

The system retrieves relevant information from the HR knowledge base
before generating the answer.

2. Retrieval-Augmented Generation

The LLM is supplied with retrieved document context rather than being
expected to answer solely from its pretrained knowledge.

This improves relevance and makes the system suitable for
organization-specific information.

3. Agent

The /agent endpoint provides a natural-language interface to the
application's agent capabilities.

4. Conversation Memory

The /ask endpoint accepts an optional conversation_id.

This allows multiple requests to be associated with the same
conversation.

5. Task Management

The application supports:

Creating tasks

Listing tasks

Retrieving a task

Updating tasks

Completing tasks

Deleting tasks

Task priorities

Task statuses

Optional due dates

6. React Frontend

The frontend provides a browser-based interface for interacting with the
backend.

The frontend API client supports a configurable backend URL through:

VITE_API_BASE_URL

7. Automated Testing

The project includes backend tests covering the implemented application
components.

Current validation:

54 passed
0 failed
1 warning

System Architecture

The application is divided into logical layers.

┌─────────────────────────────────────────────┐
│                  Frontend                   │
│              React + Vite                   │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│                 API Layer                   │
│                  FastAPI                    │
├─────────────────────────────────────────────┤
│ /ask     /agent     /tasks     /health      │
└──────┬──────────────┬──────────────┬────────┘
       │              │              │
       ▼              ▼              ▼
┌────────────┐  ┌────────────┐  ┌────────────┐
│     QA     │  │   Agent    │  │   Tasks    │
│   / RAG    │  │   Tools    │  │  Service   │
└─────┬──────┘  └─────┬──────┘  └────────────┘
      │               │
      ▼               ▼
┌────────────┐  ┌────────────┐
│ Vectorstore│  │  Memory    │
│   / FAISS  │  │ Repository │
└─────┬──────┘  └────────────┘
      │
      ▼
┌────────────┐
│ HR Docs    │
└────────────┘

Request Flow

HR Question

A typical /ask request follows this flow:

User
 ↓
React UI
 ↓
POST /ask
 ↓
FastAPI
 ↓
Question processing
 ↓
Embedding / semantic retrieval
 ↓
FAISS similarity search
 ↓
Relevant HR document context
 ↓
LLM prompt
 ↓
Groq
 ↓
Generated answer
 ↓
Conversation memory update
 ↓
JSON response
 ↓
React UI

Agent Request

User
 ↓
React UI / API client
 ↓
POST /agent
 ↓
Agent
 ↓
Available tools / application capabilities
 ↓
Result
 ↓
Response

Task Request

React UI
 ↓
FastAPI
 ↓
Task route
 ↓
Task service
 ↓
Task repository
 ↓
Task response

Technology Stack

Backend

Technology              Purpose

Python 3.11.9           Backend runtime
FastAPI                 REST API
Uvicorn                 ASGI server
Pydantic                Data validation
python-dotenv           Environment configuration
FAISS CPU               Vector similarity search
Sentence Transformers   Embeddings
Transformers            Model infrastructure
PyTorch                 ML runtime
scikit-learn            ML utilities
SciPy                   Scientific/ML dependencies
PyPDF                   PDF processing
Groq                    LLM inference

Frontend

Technology   Purpose

React 19     UI
React DOM    Browser rendering
Vite 8       Development/build tooling
JavaScript   Frontend implementation

Project Structure

p7/
│
├── app/
│
├── backend/
│   ├── agent/
│   │   ├── ...
│   │   └── test_agent.py
│   │
│   ├── data/
│   │   └── hr_documents/
│   │       ├── benefits_policy.txt
│   │       ├── employee_handbook.txt
│   │       ├── it_setup_guide.txt
│   │       └── security_policy.txt
│   │
│   ├── ingestion/
│   │   ├── ...
│   │   └── test_retrieve.py
│   │
│   ├── memory/
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   └── tests
│   │
│   ├── qa/
│   │   ├── ...
│   │   └── answer.py
│   │
│   ├── tasks/
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── routes.py
│   │   ├── service.py
│   │   └── tests
│   │
│   ├── vectorstore/
│   │   └── ...
│   │
│   ├── main.py
│   └── test_main.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   └── services/
│   │       └── api.js
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── tests/
│
├── .env.example
├── .gitignore
├── .python-version
├── requirements.txt
└── README.md

HR Knowledge Base

The current repository includes:

backend/data/hr_documents/

with:

benefits_policy.txt
employee_handbook.txt
it_setup_guide.txt
security_policy.txt

These documents represent the controlled knowledge source for the HR
assistant.

The RAG system should use these documents as the authoritative context
for organization-specific HR questions.

RAG Pipeline

The Retrieval-Augmented Generation architecture separates retrieval from
generation.

Step 1 --- Source Documents

HR documents are stored in the repository.

HR documents
    ↓
Document loading

Step 2 --- Text Processing

Documents are processed into searchable text units.

Documents
    ↓
Text extraction
    ↓
Text splitting
    ↓
Chunks

Step 3 --- Embeddings

Text chunks are converted into numerical vector representations.

Text chunk
    ↓
Embedding model
    ↓
Vector

Step 4 --- Vector Store

Embeddings are stored in FAISS.

Embedding vectors
       ↓
     FAISS

Step 5 --- Retrieval

When the user asks a question:

Question
   ↓
Question embedding
   ↓
FAISS similarity search
   ↓
Top relevant chunks

Step 6 --- Generation

Retrieved context is supplied to the LLM.

Question
   +
Retrieved context
   ↓
LLM
   ↓
HR answer

This architecture is preferable to asking the LLM to answer
organization-specific questions without retrieval.

Agent Layer

The agent provides a higher-level natural-language interface to
application capabilities.

Endpoint:

POST /agent

Request:

{
  "message": "..."
}

The agent layer is separated from the HTTP layer so that application
capabilities can be extended independently.

Conversation Memory

Conversation memory is exposed through the /ask endpoint.

Request:

{
  "question": "What does the leave policy say?",
  "conversation_id": "demo-conversation"
}

A subsequent request can reuse the same conversation identifier:

{
  "question": "Summarize that in one sentence.",
  "conversation_id": "demo-conversation"
}

Conceptually:

Conversation ID
      ↓
Memory lookup
      ↓
Previous context
      +
Current question
      ↓
Answer
      ↓
Updated memory

The memory layer is separated into models, repository, and service
responsibilities.

Task Management

The task system provides a REST-based task lifecycle.

Task model

Tasks support:

title
description
status
priority
due_date
created_at
id

Status values

todo
in_progress
completed

Priority values

low
medium
high

Lifecycle

Create
  ↓
todo
  ↓
in_progress
  ↓
completed

Tasks can also be updated or deleted.

FastAPI API

GET /health

Returns the API health status.

Example:

Invoke-WebRequest http://127.0.0.1:8000/health -UseBasicParsing

Expected HTTP status:

200 OK

POST /ask

Answers an HR question using RAG and optional conversation memory.

Request:

{
  "question": "What is the company's leave policy?",
  "conversation_id": "optional-id"
}

POST /agent

Processes a natural-language request through the HR agent.

Request:

{
  "message": "Help me with an HR request."
}

GET /tasks

Returns available tasks.

POST /tasks

Creates a task.

Example:

{
  "title": "Review employee handbook",
  "description": "Review the latest HR policy document.",
  "priority": "high"
}

GET /tasks/{task_id}

Retrieves a specific task.

PATCH /tasks/{task_id}

Updates a task.

Example:

{
  "status": "in_progress"
}

DELETE /tasks/{task_id}

Deletes a task.

POST /tasks/{task_id}/complete

Marks a task as completed.

React Frontend

The frontend is implemented with React and Vite.

The frontend communicates with the FastAPI backend through:

frontend/src/services/api.js

The API base URL is configurable:

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

This provides two modes:

Local development

VITE_API_BASE_URL not set
        ↓
http://127.0.0.1:8000

Deployment

VITE_API_BASE_URL=https://your-backend-domain

This prevents the deployed browser from attempting to access its own
localhost.

Environment Configuration

The project requires a Groq API key.

.env.example:

GROQ_API_KEY=your_groq_api_key_here

For local development, create:

.env

with:

GROQ_API_KEY=your_real_key

Do not commit the real .env file.

The frontend must never contain the Groq API key.

Local Installation

1. Clone

git clone https://github.com/THOTALINGESWARARAO/supervity-p7.git
cd supervity-p7

2. Create virtual environment

python -m venv .venv

Activate:

.\.venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

4. Configure environment

Create .env:

GROQ_API_KEY=your_groq_api_key_here

5. Install frontend dependencies

cd frontend
npm install
cd ..

Running the Application

Backend

From the project root:

.\.venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload

Backend:

http://127.0.0.1:8000

Swagger UI:

http://127.0.0.1:8000/docs

OpenAPI JSON:

http://127.0.0.1:8000/openapi.json

Frontend

In another terminal:

cd frontend
npm run dev

Use the URL printed by Vite.

API Examples

Ask an HR question

PowerShell:

$body = @{
    question = "What is the company's leave policy?"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri http://127.0.0.1:8000/ask `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

Ask with conversation memory

$body = @{
    question = "What does the leave policy say?"
    conversation_id = "demo-conversation"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri http://127.0.0.1:8000/ask `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

Follow-up:

$body = @{
    question = "Can you summarize that?"
    conversation_id = "demo-conversation"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri http://127.0.0.1:8000/ask `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

Create a task

$body = @{
    title = "Review HR handbook"
    description = "Review the current employee handbook."
    priority = "high"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri http://127.0.0.1:8000/tasks `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

List tasks

Invoke-RestMethod http://127.0.0.1:8000/tasks

Testing and Validation

Run:

pytest -q

Current result:

54 passed
1 warning

There are currently no failing tests.

The warning observed during testing is:

StarletteDeprecationWarning:
Using `httpx` with `starlette.testclient` is deprecated;
install `httpx2` instead.

This warning does not currently affect the test result.

Frontend Production Build

The frontend was validated with:

cd frontend
npm run build

The production build completed successfully.

Typical generated output:

dist/
├── index.html
└── assets/

The generated dist directory is a build artifact and is not required
to be committed when the deployment platform builds the frontend itself.

Task 10 Full Integration

Task 10 focused on validating that the previously implemented components
work together rather than only passing isolated unit tests.

Integration chain

Frontend
   ↓
FastAPI
   ↓
Question / Agent / Task API
   ↓
Application services
   ↓
RAG / Memory / Tasks
   ↓
External LLM where applicable
   ↓
Response
   ↓
Frontend

Validation performed

Automated backend suite

54 passed

Backend startup

Application startup complete.

Health endpoint

GET /health
→ 200 OK

OpenAPI

The live backend exposed the expected application routes:

/tasks
/tasks/{task_id}
/tasks/{task_id}/complete
/agent
/health
/ask

RAG endpoint

A live request to:

POST /ask

successfully returned an HR answer based on the application's knowledge
base.

Frontend build

npm run build
→ successful

This establishes that the application was successfully integrated and
validated locally before deployment.

Deployment Status

A Render deployment was attempted for the FastAPI backend.

Build result

The Render build completed successfully.

Build successful

Runtime result

The service could not remain running on the Render Free instance because
the application exceeded the available 512 MB memory limit while
starting the AI/model stack.

Observed runtime error:

Out of memory (used over 512Mi)

The deployment was intentionally stopped rather than misrepresenting the
application as successfully deployed.

Important distinction

This is an infrastructure/resource limitation, not a failing application
test.

Local result:

54/54 tests passing

Local runtime:

FastAPI startup successful
Model loading successful
/health successful
/ask successful

Deployment runtime:

Render Free instance
       ↓
512 MB memory
       ↓
PyTorch + Transformers + Sentence Transformers + FAISS
       ↓
Out of memory

Deployment Considerations

The current architecture loads ML dependencies and model components in
the backend process.

The dependency stack includes:

torch
transformers
sentence-transformers
faiss-cpu
scikit-learn
scipy

This is significantly heavier than a conventional lightweight FastAPI
application.

A future production deployment should use an environment with sufficient
memory.

Potential approaches include:

Option 1 --- Larger backend instance

Use a deployment instance with enough RAM for model initialization and
runtime.

Option 2 --- Separate inference service

Move embedding/model inference into a dedicated service.

Frontend
   ↓
FastAPI
   ↓
Inference Service
   ↓
Embedding / Model

Option 3 --- External embedding/inference API

Use a managed embedding/inference provider instead of loading the full
model stack inside the web service.

Option 4 --- Optimize the model stack

Reduce memory usage through:

Smaller embedding models

Lazy model loading

More efficient model formats

Reduced worker count

Avoiding duplicate model instances

These are future infrastructure improvements and are not required to
establish the correctness of the current local implementation.

Production Environment

For a backend deployment, the server should bind to the
platform-provided port.

Example:

uvicorn backend.main:app --host 0.0.0.0 --port $PORT

Required backend environment variable:

GROQ_API_KEY=...

For the frontend:

VITE_API_BASE_URL=https://your-backend-domain

The frontend build should then be:

npm run build

Security

API keys

Never commit:

.env

Never place:

GROQ_API_KEY

inside React source code.

The browser must communicate only with the backend API.

Environment separation

Development:

.env

Deployment:

Platform environment variables

Template:

.env.example

Troubleshooting

Backend does not start

Check:

python --version

Expected:

Python 3.11.x

Install dependencies again:

pip install -r requirements.txt

Groq API errors

Verify:

GROQ_API_KEY

is present in the environment.

Do not expose the key in source code or frontend files.

Frontend cannot reach backend

Check:

VITE_API_BASE_URL

For local development, the fallback is:

http://127.0.0.1:8000

For deployment, it must point to the public backend URL.

Render deployment runs out of memory

If the deployment reports:

Out of memory (used over 512Mi)

the instance does not have sufficient RAM for the current ML stack.

This is not fixed by changing the FastAPI port or adding HF_TOKEN.

Use a larger instance or redesign the model/inference layer.

Hugging Face unauthenticated warning

A local/deployment startup warning may indicate that requests to the
Hugging Face Hub are unauthenticated.

This can affect download rate limits.

It is separate from the Render 512 MB out-of-memory failure.

Development Workflow

Recommended workflow:

1. Activate .venv
2. Start backend
3. Start frontend
4. Implement changes
5. Run pytest
6. Run frontend build
7. Test the affected API
8. Inspect git status
9. Commit
10. Push

Backend test:

pytest -q

Frontend build:

cd frontend
npm run build
cd ..

Git verification:

git status
git log -1 --oneline

A clean repository should report:

nothing to commit, working tree clean

Project Status

Component                        Status

Backend foundation               Complete
HR document ingestion            Complete
Vector retrieval                 Complete
RAG question answering           Complete
Agent                            Complete
Task management                  Complete
Conversation memory              Complete
FastAPI integration              Complete
React frontend                   Complete
Frontend API integration         Complete
Automated tests                  54/54 passing
Local end-to-end validation      Complete
Frontend production build        Passing
Production backend deployment    Pending
Production frontend deployment   Pending
Infrastructure optimization      Pending

Milestone Summary

Tasks 1--5

Core application foundation and knowledge-assistant functionality
established.

Task 6 --- Task Management

Implemented:

Task models

Repository

Service

Routes

Task lifecycle

Tests

Task 7 --- Agent Tools

Implemented and validated the agent/tool layer.

Task 8 --- Conversation Memory

Implemented:

Memory models

Repository

Service

Conversation-aware API behavior

Tests

Task 9 --- React Frontend

Implemented:

React application

Vite build

API client

HR interaction UI

Task interaction UI

Production build

Task 10 --- Full Integration

Validated:

Backend
+
RAG
+
Agent
+
Memory
+
Tasks
+
Frontend

with:

54 tests passing

Current Git State

The deployment-preparation commit was created and pushed successfully.

Latest deployment-preparation commit:

d6e2076 chore: prepare application for deployment

The commit includes:

Environment-driven frontend API configuration

Python 3.11.9 deployment pin

The repository was clean after the push.

Repository

GitHub:

https://github.com/THOTALINGESWARARAO/supervity-p7

Conclusion

P7 demonstrates a complete AI application engineering workflow:

                 ┌───────────────────┐
                 │   HR Documents    │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Ingestion +       │
                 │ Embeddings        │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ FAISS Vector      │
                 │ Store             │
                 └─────────┬─────────┘
                           │
                           ▼
┌──────────────┐   ┌───────────────────┐
│ React        │──▶│ FastAPI           │
│ Frontend     │   │ Application       │
└──────────────┘   └─────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
           RAG / QA        Agent         Tasks
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                      Conversation
                         Memory
                             │
                             ▼
                         Groq LLM

The application is locally integrated and validated. The remaining
deployment limitation is infrastructure capacity: the selected Render
Free instance cannot provide enough memory for the current local AI
model stack.

The project therefore reaches a clean engineering checkpoint:

Implementation        ✅
Integration           ✅
Automated testing     ✅
Local runtime         ✅
Frontend build        ✅
Deployment attempt    ✅
Production deployment ⚠️ Infrastructure-limited
