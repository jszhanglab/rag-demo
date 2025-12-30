# Database Schema (ER Diagram)
This ER diagram describes the core relational structure for the RAG demo:
- `users`: system users (document owners, admins, audit)
- `documents`: uploaded files and their metadata
- `ocr_results`: OCR text
- `chunks`: text chunks generated from ocr_results for retrieval

```mermaid
erDiagram
  USERS ||--o{ DOCUMENTS : "owns"
  DOCUMENTS ||--o{ OCR_RESULTS : "has"
  OCR_RESULTS ||--o{ CHUNKS : "contains"

  USERS {
    uuid id PK
    string email
    string name
    string role
    boolean is_active
    datetime created_at
    datetime updated_at
    uuid updated_by_user_id FK
    datetime deleted_at
    uuid deleted_by_user_id FK
  }

  DOCUMENTS {
    uuid id PK
    uuid user_id FK
    string filename
    string mime_type
    bigint file_size_bytes
    string status
    string source
    text error_message
    datetime created_at
    uuid created_by_user_id FK
    datetime updated_at
    uuid updated_by_user_id FK
    datetime deleted_at
    uuid deleted_by_user_id FK
  }

  OCR_RESULTS {
    uuid id PK
    uuid document_id FK
    text text
    jsonb table_data
    string status
    text error_message
    datetime created_at
    datetime updated_at
    uuid created_by_user_id FK
    uuid updated_by_user_id FK
  }

  CHUNKS {
    uuid id PK
    uuid ocr_result_id FK
    int chunk_index
    int start_offset
    int end_offset
    int token_count
    text text
    string embedding_id
    datetime created_at
  }
```  

# 📊 Entity Relationships and Deletion Strategy Design

This document outlines the relationships between the three core entities in the RAG system: User, Document, and Chunk, as well as the adopted deletion strategy.

---
## 🔗 Entity Relationships

| Parent Entity | Child Entity | Relationship Description | Foreign Key Definition |
| :--- | :--- | :--- | :--- |
| `users` | `documents` | **One-to-Many**: A user owns many documents. | `documents.user_id` → `users.id` |
| `documents` | `ocr_results` | **One-to-One**: A document has only one ocr text. | `ocr_results.document_id` → `documents.id` |
| `ocr_results` | `chunks` | **One-to-Many**: A ocr_results contains many data chunks. | `ocr_results.document_id` → `documents.id` |
---

## 🗑️ Deletion Strategy

### 1. Hard Delete (Physical Deletion)

The following relationship utilizes **cascading physical deletion** to ensure strong consistency and retrieval performance between chunks and their parent document:

* **Document Deletion Cascade:** When a record in the `documents` table is **physically deleted**, all associated `chunks` `ocr_results` records are automatically and permanently deleted by the database.
    * **Constraint:** `chunks.document_id` has the `ON DELETE CASCADE` attribute.

### 2. Soft Delete (Logical Deletion)

The following entities implement a **logical deletion** mechanism (soft delete) to retain history and support data recovery features:

| Entity | Logical Deletion Marker Columns | Purpose |
| :--- | :--- | :--- |
| `users` | `users.deleted_at` | Records the timestamp of deletion. Non-NULL indicates the record has been logically deleted. |
| `users` | `users.deleted_by_user_id` | Records the ID of the user who performed the deletion, for auditing. |
| `documents` | `documents.deleted_at` | Records the timestamp of deletion. Non-NULL indicates the record has been logically deleted. |
| `documents` | `documents.deleted_by_user_id` | Records the ID of the user who performed the deletion, for auditing. |

**Note:**
* When a `documents` record is **logically deleted** (i.e., updating `deleted_at`), its associated `chunks` are **not** automatically deleted.
* Application logic should simultaneously call the code to **physically delete** the associated `chunks` when a document is logically deleted, to maintain the performance of the RAG retrieval system.

## Table Definitions (DDL)
```sql
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE,
  name VARCHAR(100),
  role VARCHAR(20) NOT NULL DEFAULT 'user',  -- 'user' | 'admin'
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by_user_id UUID NULL REFERENCES users(id),
  deleted_at TIMESTAMPTZ NULL,
  deleted_by_user_id UUID NULL REFERENCES users(id)
);


CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),       -- document owner
  filename VARCHAR(255) NOT NULL,
  file_path TEXT NOT NULL,
  mime_type VARCHAR(100),
  file_size_bytes BIGINT,
  status VARCHAR(50) NOT NULL,                      -- uploaded | processing | ready | failed
  source VARCHAR(50) NOT NULL,                      -- upload | api | url
  error_message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by_user_id UUID NULL REFERENCES users(id),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by_user_id UUID NULL REFERENCES users(id),
  deleted_at TIMESTAMPTZ NULL,
  deleted_by_user_id UUID NULL REFERENCES users(id)
);

CREATE TABLE ocr_results (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  text TEXT NOT NULL,                                 -- OCR text
  table_data JSONB,                                   -- table metadata
  status VARCHAR(50) NOT NULL DEFAULT 'processing',   -- processing | completed | failed
  error_message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by_user_id UUID NULL REFERENCES users(id),
  updated_by_user_id UUID NULL REFERENCES users(id)
);

CREATE TABLE chunks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  chunk_index INT NOT NULL, --The sequential position of this chunk within the same document.
  start_offset INT,
  end_offset INT, 
  token_count INT,
  text TEXT NOT NULL,
  embedding_id VARCHAR(255), --The association between chunks and vector DB. 
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

