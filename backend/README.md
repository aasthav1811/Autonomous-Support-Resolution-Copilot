# 🤖 Customer Support Resolution Copilot

### Multi-Agent AI · LangGraph · RAG · Groq (free) · MCP · Docker

A multi-agent support ticket pipeline: every ticket flows through intake
(classification), routing, RAG retrieval over a knowledge base, reply
drafting, escalation checks, and a follow-up decision — with a hallucination
check on the drafted reply.

```text
Ticket Input
     │
     ▼
Intake Agent (LLM: category / urgency / sentiment)
     │
     ▼
Routing Agent (team assignment)
     │
     ▼
Retrieval Agent (RAG over ChromaDB)
     │
     ▼
Drafting Agent (LLM: reply grounded in KB)
     │
     ▼
Escalation Agent
     │
     ▼
Follow-Up Agent
     │
     ▼
Final Response + Hallucination Check
```

## Tech Stack

| Component           | Technology                                     |
| ------------------- | ---------------------------------------------- |
| LLM                 | Groq free tier (default), Claude API, or Ollama|
| Embeddings          | all-MiniLM-L6-v2 (ONNX, bundled with ChromaDB) |
| Vector Database     | ChromaDB                                       |
| Agent Orchestration | LangGraph                                      |
| Backend API         | FastAPI                                        |
| Agent Interface     | MCP server (Model Context Protocol)            |
| Frontend UI         | Next.js (plus a Streamlit dev UI)              |
| Packaging           | Docker + docker-compose                        |

---

## Quick Start (Docker — recommended)

From the **repository root** (one level above this folder):

```bash
cp .env.example .env        # then paste your real GROQ_API_KEY into .env
docker compose up --build
```

That starts three services:

| Service  | URL                        | What it is                   |
| -------- | -------------------------- | ---------------------------- |
| api      | http://localhost:8000/docs | FastAPI backend (Swagger UI) |
| frontend | http://localhost:3000      | Next.js UI                   |
| mcp      | http://localhost:8001/mcp  | MCP server (Streamable HTTP) |

Get a free API key at https://console.groq.com/keys. The default model is
`llama-3.3-70b-versatile` (override with `GROQ_MODEL`). To use the Claude API
instead, set `LLM_PROVIDER=anthropic` and `ANTHROPIC_API_KEY`.

---

## Local Development (no Docker)

```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env         # add your GROQ_API_KEY

# One-time: build the vector store
python -m src.rag.ingest

# Run the API
uvicorn api.main:app --reload --port 8000

# Or the Streamlit dev UI
streamlit run ui/app.py
```

Then in `frontend/`:

```bash
npm install
npm run dev                  # http://localhost:3000
```

Test the API directly:

```bash
curl -X POST http://localhost:8000/process_ticket \
  -H "Content-Type: application/json" \
  -d '{"ticket_id":"T100","customer_email":"a@b.com","subject":"Refund please","body":"I was charged twice and would like a refund."}'
```

### Using Ollama instead (free, local-only)

The Ollama path still works for offline development. In `.env`:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5-coder:7b
```

Then run `ollama serve` and `ollama pull qwen2.5-coder:7b`. Note this only
works on your machine — cloud deployments should use `groq` or `anthropic`.

---

## MCP Server

The copilot is also exposed as an **MCP tool**, so any MCP-capable client
(Claude, Claude Code, other agents) can call the pipeline directly:

```bash
python api/mcp_server.py     # serves http://localhost:8001/mcp
```

It exposes one tool, `process_ticket(ticket_id, customer_email, subject,
body)`, returning the full pipeline output. To try it from Claude Code:

```bash
claude mcp add --transport http support-copilot http://localhost:8001/mcp
```

---

## Deploying Online

The backend is a standard Docker container, so any container host works:

- **Render / Railway** — create a web service from this repo, point it at
  `backend/Dockerfile`, set `GROQ_API_KEY` and `CORS_ORIGINS`
  env vars. Port 8000.
- **Fly.io** — `fly launch` inside `backend/`.
- **Frontend on Vercel** — deploy the `frontend/` folder and set
  `NEXT_PUBLIC_API_URL` to your deployed API URL (it's inlined at build
  time). Then add the Vercel URL to the backend's `CORS_ORIGINS`.

The knowledge base is baked into the image at build time (`RUN python -m
src.rag.ingest` in the Dockerfile), so containers start instantly with no
runtime downloads.

---

## Environment Variables

| Variable            | Default                  | Purpose                                 |
| ------------------- | ------------------------ | --------------------------------------- |
| `LLM_PROVIDER`      | `groq`                   | `groq`, `anthropic`, or `ollama`        |
| `GROQ_API_KEY`      | —                        | Required for Groq (free tier)           |
| `GROQ_MODEL`        | `llama-3.3-70b-versatile`| Any Groq model ID                       |
| `ANTHROPIC_API_KEY` | —                        | Claude API only                         |
| `ANTHROPIC_MODEL`   | `claude-opus-4-8`        | Claude API only                         |
| `CORS_ORIGINS`      | `http://localhost:3000`  | Comma-separated allowed browser origins |
| `OLLAMA_BASE_URL`   | `http://localhost:11434` | Ollama only                             |
| `OLLAMA_MODEL`      | `llama3.2`               | Ollama only                             |
| `MCP_PORT`          | `8001`                   | MCP server port                         |

---

## Troubleshooting

**`api_key: MISSING` in /health** — set `GROQ_API_KEY` (or `ANTHROPIC_API_KEY`
for the Claude provider) in your `.env` — or the compose `.env` at the repo
root — and restart.

**Browser shows "Cannot reach the API"** — the frontend was built with the
wrong `NEXT_PUBLIC_API_URL`, or the API's `CORS_ORIGINS` doesn't include the
frontend's origin.

**ChromaDB errors after upgrading** — the embedding pipeline changed from
sentence-transformers to ChromaDB's built-in ONNX model. Rebuild the store:

```bash
rm -rf chroma_db/ && python -m src.rag.ingest
```

**`ModuleNotFoundError: No module named 'src'`** — run commands from the
`backend/` project root.

---

## Skills Demonstrated

* Multi-Agent Orchestration with LangGraph
* Retrieval-Augmented Generation (RAG)
* Provider-swappable LLM layer (Groq / Claude API / Ollama)
* MCP (Model Context Protocol) server
* Vector Databases with ChromaDB
* FastAPI Backend Development
* Dockerized deployment (multi-service compose)
* Human-in-the-Loop AI Systems
* Prompt Engineering & Hallucination Checking
