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