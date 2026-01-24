# Development Log

## 2025-11-05
- Completed initial project structure setup:
  - `web/`: Next.js frontend
  - `gateway/`: Node.js gateway
  - `rag-service/`: FastAPI RAG core service
  - `docs/`: Mind maps and design documentation
- Initialized `web/` project.
- Imported mind maps.

## 2025-11-07
- Refactored project structure to support i18n and monorepo layout.

## 2025-11-12
- Completed the base layout structure, including header, main container, and three-column UI layout.

## 2025-11-18
- Added collapsible sidebar with toggle button and state management.
- Verified layout responsiveness and basic UI interactions.

## 2025-11-21
- Completed the upload layout.

## 2025-11-27
- Completed frontend (Next.js) integration with backend (FastAPI).
- Implemented the first end-to-end data fetch flow, verifying communication between the web app and the API service.

## 2025-11-29
- Refactored API structure for monorepo architecture.
- Created shared `apiRoutes.json` under `packages/common` to centralize API route definitions used by both frontend and backend.

## 2025-12-02
- Completed backend implementation for file upload (FastAPI endpoint + handling logic).
- Introduced Poetry to manage the FastAPI project environment and dependencies.

## 2025-12-03
- Completed Docker setup for PostgreSQL, including:
  - Running PostgreSQL via Docker container
  - Preparing environment for schema initialization and metadata storage
  - Verifying connectivity from host environment to container

## 2025-12-05
- Troubleshot PaddleOCR initialization issues
- Resolved VSCode/Poetry environment inconsistencies
- Cleaned up backend structure to ensure stable module imports

## 2025-12-12
- Completed file upload service and repository implementation.
  - Built ORM class for document handling.
  - Implement Sqlalchemy ORM framework for database operation.
  - Developed the document repository for managing file metadata.
- Temporarily use a mock user on backend before auth is implemented.
- Fixed frontend upload bug that prevented correct error tips from showing.

## 2025-12-16
- Implemented SWR for efficient communication between different components in the project. This improves data fetching and synchronization between UI components.

## 2025-12-17
- Completed around 50% of the Sidebar component, focusing on UI/UX and interactive elements. Realized the importance of prioritizing the chunking and embedding services before completing the Sidebar.
- Cleaned up the mock user fetch method, ensuring a cleaner and more efficient mock data handling for the development environment.

## 2025-12-20
- Completed OCR flow by PaddleOCR.

## 2025-12-25
- Refactored the pipeline flow to ensure smooth coordination between tasks such as OCR, chunking, and embedding.
- Manually implemented the LangChain structure, handling text splitting and processing logic to increase flexibility and scalability in document processing.

## 2025-12-30
- Completed chunk flow by langchain-text-splitters library.

## 2025-12-31
- Refactor chunk token calculation using the Transformers tokenizer.

## 2026-01-02
- Implemented vector store abstraction and embedding repository.
- Defined metadata schema for chunk-level vector indexing.

## 2026-01-16
- Completed the end-to-end embedding pipeline (OCR → Chunk → Embedding).
- Integrated embedded Chroma as a local vector index with persistent storage.
- Successfully indexed chunk embeddings and metadata to disk.

## 2026-01-17
- Completed the search pipeline
  - Implemented the full search pipeline including embedding query, vector search with Chroma, and retrieving relevant chunk data from PostgreSQL.
  - Successfully integrated vector database and chunk repository to provide accurate search results.
- Resolved .env file configuration issue
  - Addressed issues with environment variable loading and ensured sensitive information (like database credentials) is correctly loaded from the .env file using Pydantic.
  - Improved .env management for different environments (development/production).

## 2026-01-21
- Implemented status-driven UI updates and refactored document-related APIs.
- Resolved several bugs in the embedding pipeline.
- Improved frontend–backend alignment by introducing concurrent processing.

## 2026-01-22
- Fixed Swagger UI exposure issues in production environment.
- Fixed the method for fetching .env configuration.