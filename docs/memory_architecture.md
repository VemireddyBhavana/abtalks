# Persistent Memory Subsystem Architecture

This document describes the design and technical architecture of the **Persistent Memory Subsystem** (Phase 8) in the **ABTalks AI Interview Agent**.

---

## 🏗️ Architectural Overview

The Persistent Memory Subsystem provides a provider-agnostic, enterprise-grade memory layer. It enables the AI Agent to persist interview sessions, remember candidate turn answers, record evaluation rubrics, track knowledge gaps, store final feedback reports, and recover session states via milestone snapshots.

```mermaid
graph TD
    subgraph Interview Engine Domain
        IE[InterviewEngine]
    end

    subgraph Service & Repository Layer
        MS[MemoryService]
        MR[MemoryRepository]
        MC[MemoryCache]
        MV[MemoryValidator]
        SS[SessionSnapshotManager]
        MSec[MemorySecurity]
        MSR[MemorySerializer]
        MSRCH[MemorySearchEngine]
    end

    subgraph Provider Layer
        AMP[AbstractMemoryRepository]
        BP[BreethProvider]
        MP[MockMemoryProvider]
        Future[Future: Redis / Postgres / Mongo]
    end

    IE -->|1. Transmit Turns & State| MS
    MS -->|Validate Schema| MV
    MS -->|Snapshot Milestone| SS
    MS -->|Encrypt Sensitive Fields| MSec
    MS -->|Cache Hot Sessions| MC
    MS -->|Persist Data| MR

    MR -->|Delegates CRUD| AMP
    AMP <|-- BP
    AMP <|-- MP
    AMP <|-- Future
```

---

## 🔑 Key Components

### 1. `MemoryRepository` (`backend/app/repositories/memory_repository.py`)
- Decouples `MemoryService` from direct provider classes.
- Communicates with underlying `AbstractMemoryRepository` providers (Breeth, Mock, etc.).

### 2. `BreethProvider` & `MockMemoryProvider` (`backend/app/memory/`)
- `BreethProvider`: Official Breeth REST/SDK API provider wrapper with automatic fallback handling.
- `MockMemoryProvider`: Deterministic in-memory repository implementation for offline testing and CI/CD.

### 3. `MemoryCache` (`backend/app/memory/memory_cache.py`)
- Caches hot `InterviewMemory` documents in RAM.
- Eliminates repeated external API calls during active multi-turn interviews.

### 4. `SessionSnapshotManager` (`backend/app/memory/session_snapshot.py`)
- Creates immutable state snapshots at critical milestones (`Interview started`, `Question answered`, `Evaluation completed`, `Interview finished`).
- Essential for debugging, audit trails, and crash recovery.

### 5. `MemorySecurity` (`backend/app/memory/memory_security.py`)
- Encrypts sensitive fields (candidate answer text) before storage and decrypts them on retrieval.
- Provider-independent security layer.

### 6. `MemorySearchEngine` (`backend/app/memory/memory_search.py`)
- Supports multi-criteria queries across sessions, candidates, topics, curriculum days, knowledge gaps, and quality classifications.

---

## 🔮 Future Extensibility

The memory layer is strictly provider-agnostic. Adding support for new databases (Redis, PostgreSQL, MongoDB, Pinecone, Weaviate) requires **zero changes** to `InterviewEngine` or `MemoryService`:

1. Implement `AbstractMemoryRepository` (e.g. `RedisMemoryProvider`).
2. Add provider option in `MemoryFactory`.
3. Set `MEMORY_PROVIDER=redis` in `.env`.
