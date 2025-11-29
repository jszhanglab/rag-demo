# Development Log

## 2025-11-5
- Completed project structure setup:
 - 'web/': Next.js frontend
 - 'gateway/': Node.js gateway
 - 'rag-service/': FastAPI RAG core service
 - 'docs/': Mind maps and design documentation
- Initialized 'web/'.
- Imported mind maps.

## 2025-11-7
- Refactored project structure to support i18n and monorepo.

## 2025-11-12
- Completed the base layout structure, including header, main container, and three-column layout.
- 
## 2025-11-18
- Added collapsible sidebar with toggle button and state management.
- Verified layout responsiveness and basic UI interactions.

## 2025-11-21
- Completed the upload layout.

## 2025-11-27
- Completed frontend (Next.js) integration with backend (FastAPI).
- Implemented the first successful data-fetch flow, verifying end-to-end communication between the web app and the API service.

## 2025-11-29
- Refactored the API structure for monorepo architecture.
- Created a shared apiRoutes.json under packages/common to centralize API route definitions used by both frontend and backend.
