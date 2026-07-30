# RepoIntel

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.139.2-009688.svg)](https://fastapi.tiangolo.com/)
[![Version](https://img.shields.io/badge/version-1.0.0-informational.svg)](app/core/config.py)
[![License](https://img.shields.io/badge/license-unlicensed-lightgrey.svg)](#license)

**RepoIntel** is a repository intelligence backend that ingests GitHub repositories, indexes their source code and documentation, and exposes retrieval-augmented generation (RAG) capabilities for code-aware question answering. The service is built as a modular FastAPI application with a layered architecture that separates HTTP routing, orchestration services, indexing pipelines, hybrid retrieval, and LangChain-based conversational chains.

The HTTP API currently exposes health checks, full repository lifecycle management (create, read, update, delete), and a repository indexing endpoint. Indexing, hybrid retrieval (FAISS + BM25), LLM integration (Groq), and Redis-backed chat history are implemented at the service and chain layers; conversational Q&A is composable programmatically but not yet exposed as a REST endpoint.

Repository: [https://github.com/barsha-git/RepoIntel](https://github.com/barsha-git/RepoIntel)

---

## Features

- **GitHub repository lifecycle management** — Clone, update (pull), retrieve, and delete GitHub repositories via `RepositoryService`, with URL validation, normalized paths under `storage/repositories/{owner}/{repo}`, and a structured exception hierarchy (`InvalidRepositoryURLError`, `RepositoryCloneError`, `RepositoryAlreadyExistsError`, `RepositoryNotFoundError`, `RepositoryUpdateError`).

- **REST repository ingestion and management**
  - `POST /api/v1/repositories/repositories:` — Clone a repository or pull latest changes if it already exists locally.
  - `GET /api/v1/repositories/{owner}/{name}` — Retrieve metadata for a locally stored repository.
  - `PATCH /api/v1/repositories/{owner}/{name}` — Pull the latest changes from the remote.
  - `DELETE /api/v1/repositories/{owner}/{name}` — Remove a repository from local storage.

- **REST repository indexing** — `POST /api/v1/indexing/{owner}/{name}/index` orchestrates the full indexing pipeline: load documents, enrich with AST metadata, chunk, build a FAISS vector store, and persist it to disk.

- **Document ingestion** — Load repository files with LangChain `DirectoryLoader` and `TextLoader`, excluding build artifacts, virtual environments, and VCS metadata (`.git`, `node_modules`, `__pycache__`, `dist`, `build`, and related paths).

- **Language-aware code chunking** — Split documents with `RecursiveCharacterTextSplitter` using Python and Markdown language profiles (1,000-character chunks, 200-character overlap) and a generic fallback for other file types via `CodeChunker`.

- **AST metadata enrichment** — Parse Python source files with the standard library `ast` module to attach imports, class names, and function names to document metadata for richer retrieval context (`ASTEnricher`).

- **Dual-index retrieval** — Persist and load both **FAISS** (dense vector) and **BM25** (sparse keyword) indexes per repository under `storage/indexes/faiss/` and `storage/indexes/bm25/`.

- **Hybrid search** — Combine FAISS and BM25 retrievers via LangChain `EnsembleRetriever` with configurable weights (default: 60% FAISS, 40% BM25) through `HybridRetriever`.

- **Semantic embeddings** — Generate L2-normalized embeddings with HuggingFace `BAAI/bge-small-en-v1.5` through `langchain-huggingface` (`EmbeddingService`).

- **Result reranking** — Optional FlashRank-based contextual compression reranking via `FlashRankReranker` to refine top-k retrieval results.

- **Multi-stage RAG chains** — Composable LangChain runnables:
  - `HistoryAwareRetriever` — Rewrites follow-up questions into standalone queries before retrieval.
  - `QuestionAnswerChain` — Stuff-documents QA chain with repository-aware system prompts.
  - `RetrievalChain` — Combines retriever and QA chain.
  - `ConversationalChain` — Wraps retrieval with Redis-backed session history via `RunnableWithMessageHistory`.

- **LLM integration** — Groq chat models via `langchain-groq` (`ChatModelService`), configured through environment variables.

- **Redis integration** — Docker Compose provisioning for Redis 7; `RedisHistoryService` (LangChain `RedisChatMessageHistory`) for conversation persistence and a lightweight `RedisCache` wrapper.

- **Structured configuration** — Environment-driven settings via `pydantic-settings`, covering application metadata, API host/port, Redis, storage paths, embedding settings, LLM provider configuration, and logging level.

- **Observability** — Colored console logging through Loguru with configurable log levels.

---

## Technologies Used

| Category | Technology | Version |
|----------|------------|---------|
| Language | Python | 3.11 |
| Web framework | FastAPI | 0.139.2 |
| ASGI server | Uvicorn | 0.51.0 |
| HTTP toolkit | Starlette | 1.3.1 |
| Validation / settings | Pydantic | 2.13.4 |
| Settings loader | pydantic-settings | 2.14.2 |
| Environment variables | python-dotenv | 1.2.2 |
| Git operations | GitPython | 3.1.54 |
| Redis client | redis (Python) | 8.0.1 |
| Redis server | Redis Alpine | 7 |
| Logging | Loguru | 0.7.3 |
| LLM orchestration | LangChain Core | — |
| LangChain integrations | langchain-classic, langchain-community | — |
| Text splitting | langchain-text-splitters | — |
| Embeddings | langchain-huggingface | — |
| LLM provider | langchain-groq | — |
| Chat history | langchain-redis | — |
| Vector search | FAISS (via langchain-community) | — |
| Keyword search | BM25 (via langchain-community) | — |
| Reranking | FlashRank (via langchain-community) | — |
| Embedding model | `BAAI/bge-small-en-v1.5` | — |
| Containerization | Docker, Docker Compose | — |

> **Note:** `requirements.txt` pins core API and infrastructure dependencies only. Indexing, retrieval, and RAG chain modules additionally require LangChain packages and runtime libraries such as `faiss-cpu`, `rank-bm25`, `flashrank`, `sentence-transformers`, `langchain-groq`, and `langchain-redis`. Install these when using the full pipeline (see [Installation](#installation)).

---

## Installation

### Prerequisites

- **Python 3.11+**
- **Git** (for cloning GitHub repositories)
- **Docker** and **Docker Compose** (recommended, for Redis)
- **Groq API key** (required for LLM-backed chains; obtain at [console.groq.com](https://console.groq.com/))
- Sufficient disk space under `STORAGE_PATH` for cloned repositories and on-disk indexes

### 1. Clone the repository

```bash
git clone https://github.com/barsha-git/RepoIntel.git
cd RepoIntel
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

Install pinned core dependencies:

```bash
pip install -r requirements.txt
```

For indexing, embedding, hybrid retrieval, and conversational chains, install the additional packages referenced by the codebase:

```bash
pip install \
  langchain-core \
  langchain-classic \
  langchain-community \
  langchain-huggingface \
  langchain-text-splitters \
  langchain-groq \
  langchain-redis \
  faiss-cpu \
  rank-bm25 \
  flashrank \
  sentence-transformers
```

### 4. Configure environment variables

Copy the example environment file and extend it with all required settings. The application settings model in `app/core/config.py` requires every variable listed below; missing values will prevent startup.

```bash
cp .env.example .env
```

Complete `.env` template (adjust values as needed):

```env
# Application
APP_NAME=RepoIntel
APP_ENV=development
DEBUG=True

# API
HOST=0.0.0.0
PORT=8000

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_URL=redis://localhost:6379/0

# Chat history
HISTORY_TTL=86400
HISTORY_KEY_PREFIX=repintel:chat:

# Storage
STORAGE_PATH=storage

# Logging
LOG_LEVEL=INFO

# Embeddings
EMBEDDING_MODEL_NAME=BAAI/bge-small-en-v1.5
EMBEDDING_MODEL_DEVICE=cpu

# LLM (Groq)
LLM_PROVIDERS=groq
LLM_MODEL=llama-3.3-70b-versatile
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=4096
GROQ_API_KEY=your_groq_api_key_here
```

| Variable | Description | Example |
|----------|-------------|---------|
| `APP_NAME` | Application display name | `RepoIntel` |
| `APP_ENV` | Runtime environment | `development` |
| `DEBUG` | Enable FastAPI debug mode | `True` |
| `HOST` | API bind host | `0.0.0.0` |
| `PORT` | API bind port | `8000` |
| `REDIS_HOST` | Redis hostname | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `REDIS_DB` | Redis database index | `0` |
| `REDIS_URL` | Redis connection URL for LangChain history | `redis://localhost:6379/0` |
| `HISTORY_TTL` | Chat history TTL in seconds | `86400` |
| `HISTORY_KEY_PREFIX` | Redis key prefix for sessions | `repintel:chat:` |
| `STORAGE_PATH` | Root path for repositories and indexes | `storage` |
| `LOG_LEVEL` | Loguru log level | `INFO` |
| `EMBEDDING_MODEL_NAME` | HuggingFace embedding model identifier | `BAAI/bge-small-en-v1.5` |
| `EMBEDDING_MODEL_DEVICE` | Compute device for embeddings | `cpu` |
| `LLM_PROVIDERS` | LLM provider identifier | `groq` |
| `LLM_MODEL` | Model name for the configured provider | `llama-3.3-70b-versatile` |
| `LLM_TEMPERATURE` | Sampling temperature | `0.1` |
| `LLM_MAX_TOKENS` | Maximum tokens in LLM responses | `4096` |
| `GROQ_API_KEY` | Groq API authentication key | — |

> **Note:** `EmbeddingService` currently hardcodes `BAAI/bge-small-en-v1.5` on CPU. The `EMBEDDING_MODEL_*` settings are defined for future use. The bundled `.env.example` contains only a subset of these variables and uses a legacy `APP_NAME` value (`CodeCompass`); extend it using the template above.

### 5. Start Redis

Redis is required for conversational history and optional caching:

```bash
docker compose up -d redis
```

This launches `redis:7-alpine` on port `6379` with a persistent volume (`redis_data`).

### 6. Create storage directories

The application expects the following layout under `STORAGE_PATH` (default: `storage/`):

```bash
mkdir -p storage/repositories storage/indexes storage/cache
```

On Windows (PowerShell):

```powershell
New-Item -ItemType Directory -Force -Path storage/repositories, storage/indexes, storage/cache
```

---

## Usage

### Start the API server

**Development (with auto-reload):**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Production-style:**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The server reads `HOST` and `PORT` from the environment when launched through process managers; the commands above use explicit flags for clarity.

### Verify the service

**Health check:**

```bash
curl http://localhost:8000/api/v1/health/
```

**Expected response:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

**Register a GitHub repository:**

```bash
curl -X POST http://localhost:8000/api/v1/repositories/repositories: \
  -H "Content-Type: application/json" \
  -d '{"github_url": "https://github.com/langchain-ai/langchain.git"}'
```

**Expected response:**

```json
{
  "message": "Repository created successfully.",
  "repository": {
    "Owner": "langchain-ai",
    "repo_name": "langchain",
    "url": "https://github.com/langchain-ai/langchain.git",
    "local_path": "storage/repositories/langchain-ai/langchain"
  }
}
```

**Index a repository:**

```bash
curl -X POST http://localhost:8000/api/v1/indexing/langchain-ai/langchain/index
```

**Expected response:**

```json
{
  "message": "Repository indexed successfully.",
  "repository": "langchain",
  "indexed_documents": 1234,
  "chunks": 1234,
  "status": "success"
}
```

**Retrieve repository metadata:**

```bash
curl http://localhost:8000/api/v1/repositories/langchain-ai/langchain
```

**Update a repository (pull latest):**

```bash
curl -X PATCH http://localhost:8000/api/v1/repositories/langchain-ai/langchain
```

**Delete a repository:**

```bash
curl -X DELETE http://localhost:8000/api/v1/repositories/langchain-ai/langchain
```

### Interactive API documentation

FastAPI generates OpenAPI documentation automatically:

| URL | Description |
|-----|-------------|
| [http://localhost:8000/docs](http://localhost:8000/docs) | Swagger UI |
| [http://localhost:8000/redoc](http://localhost:8000/redoc) | ReDoc |
| [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json) | OpenAPI schema |

### Programmatic usage (chain layer)

The following example illustrates how to compose the conversational RAG pipeline. This workflow is not yet exposed as a dedicated REST endpoint.

**Compose hybrid retrieval and conversational RAG chain:**

```python
from app.models.llm import ChatModelService
from app.retrieval.Embedding_Service import EmbeddingService
from app.retrieval.Faiss_store import FAISSStore
from app.retrieval.bm25_store import BM25Store
from app.retrieval.hybrid import HybridRetriever
from app.chains.history_aware_retriever import HistoryAwareRetriever
from app.chains.qa_chain import QuestionAnswerChain
from app.chains.retrieval_chain import RetrievalChain
from app.chains.conversational_chain import ConversationalChain
from app.memory.redis_history import RedisHistoryService
from app.services.repository_service import RepositoryService

repo = RepositoryService().get_repository("langchain-ai", "langchain")
llm = ChatModelService().model

embedding_service = EmbeddingService()
faiss_store = FAISSStore(embedding_service)
bm25_store = BM25Store()

faiss = faiss_store.load(repo)
bm25 = bm25_store.load(repo)

hybrid = HybridRetriever().create(
    faiss_store.as_retriever(faiss, k=5),
    bm25_store.as_retriever(bm25),
)

history_aware = HistoryAwareRetriever(llm).create(hybrid)
qa_chain = QuestionAnswerChain(llm).create()
retrieval_chain = RetrievalChain(history_aware, qa_chain).create()

conversational = ConversationalChain(
    retrieval_chain,
    RedisHistoryService(),
).create()

response = conversational.invoke(
    {"input": "How is hybrid retrieval configured?"},
    config={"configurable": {"session_id": "user-123"}},
)
print(response["answer"])
```

### Docker

A `Dockerfile` targeting Python 3.11 is provided. **Note:** the Dockerfile references `pyproject.toml`, which is not present in the repository. Use `requirements.txt`-based installation for local development until the container build is aligned with the project layout.

```bash
docker compose up -d redis
# Build and run the API container after aligning Dockerfile with requirements.txt
```

---

## Project Structure

```
RepoIntel/
├── app/
│   ├── __init__.py
│   ├── main.py                         # FastAPI application factory and entry point
│   ├── api/
│   │   ├── dependencies.py             # FastAPI dependency providers
│   │   └── routes/
│   │       ├── health.py               # Health check endpoint
│   │       ├── repository.py           # Repository CRUD endpoints
│   │       └── indexing.py             # Repository indexing endpoint
│   ├── cache/
│   │   └── redis_cache.py              # Redis-backed cache wrapper
│   ├── chains/
│   │   ├── conversational_chain.py     # RunnableWithMessageHistory wrapper
│   │   ├── history_aware_retriever.py    # Follow-up question contextualization
│   │   ├── qa_chain.py                 # Stuff-documents QA chain builder
│   │   └── retrieval_chain.py          # Retriever + QA chain composition
│   ├── core/
│   │   ├── config.py                   # Pydantic settings (environment-driven)
│   │   ├── constants.py                # Storage path constants
│   │   ├── exception.py                # Domain-specific exception hierarchy
│   │   └── logging.py                  # Loguru configuration
│   ├── indexing/
│   │   ├── ast_enricher.py             # Python AST metadata extraction
│   │   ├── CodeChunker.py              # Language-aware document chunking
│   │   ├── metadata.py                 # Document metadata dataclass
│   │   ├── repository_loader.py        # LangChain-based file loader
│   │   └── vectorstore.py              # In-memory vector store (development stub)
│   ├── memory/
│   │   └── redis_history.py            # Redis-backed chat history service
│   ├── models/
│   │   ├── llm.py                      # Groq chat model service
│   │   └── repository.py               # Repository dataclass
│   ├── prompts/
│   │   ├── contextualize_prompt.py     # History-aware retrieval prompt
│   │   ├── qa_prompt.py                # Question-answering prompt template
│   │   └── SystemPrompt.py             # RepoIntel system prompt
│   ├── retrieval/
│   │   ├── bm25_store.py               # BM25 index persistence and retrieval
│   │   ├── Embedding_Service.py        # HuggingFace embedding service
│   │   ├── Faiss_store.py              # FAISS index persistence and retrieval
│   │   ├── hybrid.py                   # FAISS + BM25 ensemble retriever
│   │   └── reranker.py                 # FlashRank contextual compression
│   ├── schemas/
│   │   ├── indexing.py                 # Pydantic models for indexing responses
│   │   └── repository.py               # Pydantic request/response models
│   └── services/
│       ├── chat_service.py             # Thin chain invocation wrapper
│       ├── indexing_service.py         # Indexing orchestration
│       └── repository_service.py       # GitHub clone/update/delete operations
├── storage/                            # Runtime data (gitignored)
│   ├── repositories/                   # Cloned Git repositories
│   ├── indexes/
│   │   ├── faiss/                      # FAISS index files per owner/repo
│   │   └── bm25/                       # Serialized BM25 retrievers
│   └── cache/                          # Application cache data
├── .env.example                        # Partial environment variable template
├── .gitignore
├── docker-compose.yml                  # Redis service definition
├── Dockerfile                          # Container image definition
├── requirements.txt                    # Pinned core Python dependencies
└── README.md
```

### Layer responsibilities

| Layer | Path | Purpose |
|-------|------|---------|
| API | `app/api/` | HTTP routing, request/response handling, dependency injection |
| Schemas | `app/schemas/` | Pydantic models for API contracts |
| Core | `app/core/` | Configuration, logging, shared constants, exceptions |
| Services | `app/services/` | Business logic orchestration across indexing, retrieval, and chat |
| Indexing | `app/indexing/` | Repository loading, chunking, AST enrichment |
| Retrieval | `app/retrieval/` | Embeddings, FAISS/BM25 stores, hybrid search, reranking |
| Chains | `app/chains/` | LangChain RAG pipeline composition |
| Prompts | `app/prompts/` | System and task-specific prompt templates |
| Models | `app/models/` | Domain data structures and LLM service |
| Cache / Memory | `app/cache/`, `app/memory/` | Redis-backed persistence helpers |

---

## API Documentation

### Base URL

```
http://localhost:8000/api/v1
```

### Authentication

No authentication is configured. All endpoints are currently open. Add API keys, OAuth, or JWT middleware before deploying to production.

### Endpoints

#### `GET /health/`

Returns application health, version, and environment.

**Request:**

```http
GET /api/v1/health/ HTTP/1.1
Host: localhost:8000
```

**Response `200 OK`:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Health indicator (`healthy`) |
| `version` | `string` | Application version from settings |
| `environment` | `string` | Value of `APP_ENV` |

---

#### `POST /repositories/repositories:`

Clone a GitHub repository or pull the latest changes if it already exists locally.

**Request:**

```http
POST /api/v1/repositories/repositories: HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "github_url": "https://github.com/owner/repo.git"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `github_url` | `string` (URL) | Yes | Valid GitHub repository URL |

**Response `200 OK`:**

```json
{
  "message": "Repository created successfully.",
  "repository": {
    "Owner": "owner",
    "repo_name": "repo",
    "url": "https://github.com/owner/repo.git",
    "local_path": "storage/repositories/owner/repo"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `message` | `string` | Operation status message |
| `repository.Owner` | `string` | GitHub organization or user |
| `repository.repo_name` | `string` | Repository name |
| `repository.url` | `string` | Original GitHub URL |
| `repository.local_path` | `string` | Local filesystem path |

---

#### `GET /repositories/{owner}/{name}`

Retrieve metadata for a locally stored repository.

**Request:**

```http
GET /api/v1/repositories/owner/repo HTTP/1.1
Host: localhost:8000
```

**Response `200 OK`:**

```json
{
  "Owner": "owner",
  "repo_name": "repo",
  "url": "https://github.com/owner/repo.git",
  "local_path": "storage/repositories/owner/repo"
}
```

---

#### `PATCH /repositories/{owner}/{name}`

Pull the latest changes from the remote repository.

**Request:**

```http
PATCH /api/v1/repositories/owner/repo HTTP/1.1
Host: localhost:8000
```

**Response `200 OK`:**

```json
{
  "message": "Repository updated successfully.",
  "repository": {
    "Owner": "owner",
    "repo_name": "repo",
    "url": "https://github.com/owner/repo.git",
    "local_path": "storage/repositories/owner/repo"
  }
}
```

---

#### `DELETE /repositories/{owner}/{name}`

Remove a repository from local storage.

**Request:**

```http
DELETE /api/v1/repositories/owner/repo HTTP/1.1
Host: localhost:8000
```

**Response `200 OK`:**

```json
{
  "message": "Repository deleted successfully.",
  "repository": {
    "Owner": "owner",
    "repo_name": "repo",
    "url": "https://github.com/owner/repo.git",
    "local_path": "storage/repositories/owner/repo"
  }
}
```

---

#### `POST /indexing/{owner}/{name}/index`

Index a locally stored repository by loading, enriching, chunking, and persisting a FAISS vector store.

**Request:**

```http
POST /api/v1/indexing/owner/repo/index HTTP/1.1
Host: localhost:8000
```

| Path parameter | Type | Description |
|----------------|------|-------------|
| `owner` | `string` | GitHub organization or user |
| `name` | `string` | Repository name |

**Response `200 OK`:**

```json
{
  "message": "Repository indexed successfully.",
  "repository": "repo",
  "indexed_documents": 1234,
  "chunks": 1234,
  "status": "success"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `message` | `string` | Operation status message |
| `repository` | `string` | Repository name |
| `indexed_documents` | `integer` | Number of document chunks indexed |
| `chunks` | `integer` | Number of chunks created |
| `status` | `string` | Indexing outcome (`success`) |

---

### Error handling

Domain exceptions from `app/core/exception.py` are raised by service-layer code but are not yet uniformly mapped to HTTP status codes by FastAPI exception handlers. Unhandled exceptions may surface as `500 Internal Server Error` responses.

| Condition | Exception |
|-----------|-----------|
| Non-GitHub or malformed URL | `InvalidRepositoryURLError` |
| Clone failure | `RepositoryCloneError` |
| Repository already exists on clone | `RepositoryAlreadyExistsError` |
| Repository not found locally | `RepositoryNotFoundError` |
| Pull/update failure | `RepositoryUpdateError` |

### Planned endpoints

Conversational Q&A is supported at the chain layer via `ConversationalChain` and `ChatService`, but a dedicated REST route (for example, `POST /chat`) is not yet registered in `app/main.py`. Consult the OpenAPI schema at `/docs` for the current route list.

---

## Testing

The repository does not currently include automated tests. The `.gitignore` is configured for common Python test artifacts (`.pytest_cache/`, `.coverage`, `htmlcov/`), indicating pytest as the intended framework. No CI pipeline or coverage reporting is configured.

### Recommended setup

```bash
pip install pytest pytest-asyncio httpx
```

### Suggested test structure

```
tests/
├── conftest.py
├── unit/
│   ├── test_repository_service.py
│   ├── test_code_chunker.py
│   └── test_ast_enricher.py
├── integration/
│   ├── test_faiss_store.py
│   ├── test_bm25_store.py
│   └── test_indexing_service.py
└── e2e/
    ├── test_health_endpoint.py
    ├── test_repository_endpoint.py
    └── test_indexing_endpoint.py
```

### Running tests (once added)

```bash
# All tests
pytest

# With coverage
pytest --cov=app --cov-report=term-missing

# End-to-end health check
pytest tests/e2e/test_health_endpoint.py -v
```

### Manual smoke test

```bash
uvicorn app.main:app --port 8000
curl -s http://localhost:8000/api/v1/health/ | python -m json.tool
```

---

## Contributing

Contributions are welcome. Please follow these guidelines:

1. **Fork and branch** — Create a feature branch from `main` (for example, `feat/chat-api`).

2. **Match existing conventions**
   - Use type hints and docstrings on public methods.
   - Place API routes under `app/api/routes/` and Pydantic models under `app/schemas/`.
   - Keep orchestration logic in `app/services/` and LangChain composition in `app/chains/`.
   - Use domain exceptions from `app/core/exception.py` for repository errors.

3. **Environment and secrets** — Never commit `.env` files or credentials. Update `.env.example` when adding new configuration keys.

4. **Dependencies** — Pin versions in `requirements.txt` when adding packages. Document any optional dependency groups in this README.

5. **Pull requests**
   - Provide a clear description of the change and motivation.
   - Reference related issues where applicable.
   - Ensure the application starts and the health endpoint responds before requesting review.

6. **Issue reporting** — Open an issue at [github.com/barsha-git/RepoIntel/issues](https://github.com/barsha-git/RepoIntel/issues) with steps to reproduce, expected behavior, and environment details (OS, Python version, dependency versions).

---

## License

No license file is included in this repository. All rights are reserved by default until a `LICENSE` file is added. Contact the repository owner before using this code in production or redistributing it.

---

## Acknowledgments

- **[FastAPI](https://fastapi.tiangolo.com/)** — High-performance async web framework and automatic OpenAPI generation.
- **[LangChain](https://python.langchain.com/)** — Document loading, text splitting, vector stores, retriever abstractions, and chain composition.
- **[Groq](https://groq.com/)** — Low-latency LLM inference for conversational Q&A.
- **[FAISS](https://github.com/facebookresearch/faiss)** — Efficient similarity search for dense vector retrieval.
- **[BM25](https://en.wikipedia.org/wiki/Okapi_BM25)** — Probabilistic keyword ranking via LangChain Community retrievers.
- **[FlashRank](https://github.com/PrithivirajDamodaran/FlashRank)** — Lightweight reranking for retrieval pipelines.
- **[HuggingFace](https://huggingface.co/)** — Embedding model hosting and `BAAI/bge-small-en-v1.5`.
- **[GitPython](https://gitpython.readthedocs.io/)** — Programmatic Git repository operations.
- **[Redis](https://redis.io/)** — In-memory data store for caching and session history.
- **[Loguru](https://github.com/Delgan/loguru)** — Structured, colorized application logging.
- **Repository maintainer:** [barsha-git](https://github.com/barsha-git) — Project author and primary contributor.
