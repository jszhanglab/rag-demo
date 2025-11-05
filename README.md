#RAG Demo

This is an end-to-end **Retrieval-Augmented Generation (RAG)** system built with:

- **Next.js** frontend (App Router)
- **Node.js Gateway** api (upload, auth, request routing)
- **FastAPI** backend(OCR, parsing, embedding, retrieval, generation)

## Features

- Document upload(PDF/image,with OCR)
- Vector search & evidence-based answer generation
- Citation display '[1][2]' + evidence sidebar
- Auditing & monitoring (planned)

## Architecture

Frontend → Gateway → Python RAG Service → VectorDB / Postgres / S3

## Run locally

```bash
cd web && npm run dev
cd gateway && node index.js
cd rag-service && uvicorn main:app --reload
```
