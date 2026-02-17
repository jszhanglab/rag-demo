# RAG Demo – End-to-End GenAI System

This project demonstrates a production-oriented **Retrieval-Augmented Generation (RAG)** system designed for document-based question answering and troubleshooting scenarios.

It simulates how GenAI can be integrated into a real-world workflow including document ingestion, OCR processing, vector search, and evidence-based answer generation.

---

## 🎯 Purpose

This demo focuses on:

- Building a full RAG pipeline from scratch
- Designing a scalable architecture with service separation
- Supporting OCR for scanned technical documents
- Enabling evidence-backed answers with citation display
- Structuring the system in a production-friendly manner

---

## 🛠 Tech Stack

**Frontend**
- Next.js (App Router)
- React
- SWR
- next-intl (i18n)
- react-pdf-viewer (PDF viewing / navigation)

**Backend**
- FastAPI + Uvicorn
- SQLAlchemy + PostgreSQL
- ChromaDB (Vector DB)
- PaddleOCR + PyMuPDF (document processing)
- sentence-transformers (embeddings)
- google-generativeai (LLM integration)

**Dev / Tooling**
- Poetry (Python dependency management)
- concurrently + wait-on (one-command local dev)

---

## 📁 Project Structure
rag-demo/
├── apps/
│ └── web/ # Next.js frontend
├── services/
│ └── rag-service/ # FastAPI backend (OCR, chunk, embedding, retrieval)
├── docs/ # Design notes / mindmap
├── package.json # Root dev orchestration (concurrently)
└── README.md
---

## 🏗 System Architecture (Current Version)
```
Frontend (Next.js)
      ↓
RAG Service (FastAPI)
      ↓
VectorDB / PostgreSQL / Storage
```
## 🔮 Planned Architecture (Production-Oriented Design)
```
Frontend
      ↓
Gateway Layer (Auth / Routing / Rate Limit)
      ↓
RAG Service
      ↓
VectorDB / DB
```
**Why Gateway?**
Although this demo directly connects frontend to the RAG service for simplicity, the architecture is designed with a future gateway layer in mind to support:
- Authentication & authorization
- Rate limiting
- Multi-tenant isolation
- Service scaling
- Zero-trust design

> ⚠ Note: The gateway layer is part of the intended production-oriented architecture.  
> The current demo version may simplify direct communication for development efficiency.
---

## 📦 Components

### 1️⃣ Frontend (Next.js)

- App Router architecture
- Document upload
- PDF viewer
- Chat interface
- Citation highlighting
- Polling-based document status tracking
- i18n-ready structure

---

### 2️⃣ RAG Service (FastAPI)

Handles:

- OCR (PaddleOCR)
- Text chunking
- Embedding generation
- Vector storage
- Retrieval pipeline
- LLM answer generation

---

## 🔄 Document Processing Flow

1. Upload document
2. Save metadata to database
3. Trigger background OCR processing
4. Store extracted text in a dedicated OCR table
5. Chunk text into semantic segments
6. Generate embeddings
7. Store vectors in VectorDB
8. Enable question answering with citation support

---

## 🧠 Key Design Decisions

### 1️⃣ Asynchronous OCR

OCR runs in the background to avoid blocking user requests and improve responsiveness.

---

### 2️⃣ Dedicated OCR Table

Each document has one stored OCR result to:

- Avoid re-processing
- Enable caching
- Improve performance
- Maintain data traceability

---

### 3️⃣ Evidence-Based Answering

**Evidence Highlighting (Current & Planned)**

Current implementation:
- Citation markers allow navigation to the corresponding PDF page.

Planned enhancement:
- Fine-grained line-level highlighting using OCR bounding box metadata.
- Each text segment will store layout coordinates during OCR processing.
- Retrieved chunks will map back to precise document locations.
- This approach enables layout-aware evidence visualization in future versions.

---
## 🔎 Citation Mapping Strategy(Technical Perspective)

**Current:**
- Page-level navigation

**Planned:**
- OCR bounding box metadata storage
- Layout coordinate tracking
- Chunk-to-layout reverse mapping

---
## 🧪 Features

- PDF / image upload with OCR
- Chunk-based vector retrieval
- Citation display
- Document status polling
- Modular backend pipeline
- Structured logging (basic)
- i18n-ready frontend

---

## 📈 Future Improvements

- Replace polling with event-driven updates (WebSocket / SSE)
- Implement fine-grained layout-aware citation highlighting
- Improve OCR table structure parsing
- Add summarization endpoint
- Introduce queue-based OCR processing (RabbitMQ / SQS)
- Add multi-document chat support
- Add cost tracking & token monitoring
- Implement full gateway layer for authentication & rate limiting

---

## 🚀 Run Locally

### Prerequisites

- Node.js (LTS recommended)
- Python 3.11
- Poetry

### 1) Install Root Dev Tools (concurrently / wait-on)

```bash
npm install
```
### 2) Install Frontend Dependencies

```bash
npm --prefix apps/web install
```
### 3) Install Backend Dependencies (Poetry)

```bash
cd services/rag-service
poetry install
cd ../../
```
### 4) Start Everything (Backend + Frontend)

```bash
npm run dev
```
This repo uses:

- concurrently to run the API and web dev servers in parallel
- wait-on to ensure the FastAPI docs endpoint is available before starting Next.js

**Root script details:**

- `dev:api` → runs `uvicorn app.main:app --reload --port 8000`
- `dev:web` → waits for `http://127.0.0.1:8000/docs` before starting Next.js

