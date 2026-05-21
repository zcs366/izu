# MemOS Docker Deployment (Session Walkthrough)

## Overview

MemOS (MemoryOS) v2.0.14 — AI memory OS for LLMs. Self-hosted via Docker with Neo4j (graph) + Qdrant (vector) + MemOS API.

## Deployment Steps

### 1. Clone & Configure

```bash
git clone https://github.com/MemTensor/MemOS.git ~/MemOS
cd ~/MemOS

# Key: .env goes in project root (not docker/), referenced by compose as env_file: ../.env
```

### 2. Provider Configuration

#### MiniMax (China-friendly, OpenAI-compatible)

| Field | Value |
|-------|-------|
| API Base | `https://api.minimax.chat/v1` |
| Chat Model | `MiniMax-Text-01` |
| Embedding Model | `embo-01` |
| Embedding Dim | `1024` |

```ini
OPENAI_API_KEY=sk-api-<your-key>
OPENAI_API_BASE=https://api.minimax.chat/v1
MOS_CHAT_MODEL=MiniMax-Text-01

MOS_EMBEDDER_MODEL=embo-01
MOS_EMBEDDER_BACKEND=universal_api
MOS_EMBEDDER_API_BASE=https://api.minimax.chat/v1
MOS_EMBEDDER_API_KEY=sk-api-<your-key>
EMBEDDING_DIMENSION=1024

# Chat API config (JSON array in one line)
CHAT_MODEL_LIST=[{"backend": "minimax", "api_base": "https://api.minimax.chat/v1", "api_key": "sk-api-<key>", "model_name_or_path": "MiniMax-Text-01", "support_models": ["MiniMax-Text-01"]}]
```

#### DeepSeek (alternative)

| Field | Value |
|-------|-------|
| API Base | `https://api.deepseek.com/v1` |
| Chat Model | `deepseek-chat` |
| Embedding | Not supported — use Jina AI or MiniMax for embeddings |

### 3. Start Infrastructure

```bash
sg docker -c 'docker compose -f docker/docker-compose.yml pull neo4j qdrant'
sg docker -c 'docker compose -f docker/docker-compose.yml up -d neo4j qdrant'
```

Neo4j health check takes ~10-30s. Verify:
```bash
sg docker -c 'docker ps --format "table {{.Names}}\t{{.Status}}"'
# Expect: neo4j-docker healthy, qdrant-docker up
```

### 4. Build & Start API Server

```bash
# Build takes 3-4 minutes (pip install in Docker)
sg docker -c 'docker compose -f docker/docker-compose.yml build memos'

# Start
sg docker -c 'docker compose -f docker/docker-compose.yml up -d memos'
```

### 5. Verify

```bash
curl http://localhost:8000/health
# Expect: {"status":"healthy","service":"memos","version":"1.0.1"}

docker logs memos-api-docker --tail 10
# Expect: "Application startup complete."
```

## Container Map

| Container | Ports | Purpose |
|-----------|-------|---------|
| neo4j-docker | 7474 (HTTP), 7687 (Bolt) | Graph DB for memory relationships |
| qdrant-docker | 6333 (REST), 6334 (gRPC) | Vector DB for embedding search |
| memos-api-docker | 8000 (REST API) | FastAPI + FastMCP server |

## Common Pitfalls

- **`.env` change not picked up**: Container reads env at start. Must recreate: `up -d --force-recreate memos`
- **Build timeout**: Docker build with pip install can take 240s+. Use background terminal with `timeout=300`.
- **No embedding model**: DeepSeek lacks embeddings. Use MiniMax (`embo-01`) or Jina AI (`jina-embeddings-v3`) for MOS_EMBEDDER_BACKEND=universal_api.
- **Neo4j auth**: Default is `neo4j/12345678`. Change `NEO4J_PASSWORD` in env.
