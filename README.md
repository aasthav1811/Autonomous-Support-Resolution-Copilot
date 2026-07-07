# 🤖 Autonomous Support Resolution Copilot

A multi-agent AI system that triages, routes, and drafts replies to customer
support tickets — with retrieval-augmented answers grounded in a knowledge
base and an automatic hallucination check on every draft.

**LangGraph · RAG (ChromaDB) · Groq LLM · FastAPI · MCP · Next.js · Docker**

## How it works

Every ticket flows through six specialized agents:

```text
Ticket ─▶ Intake ─▶ Routing ─▶ Retrieval (RAG) ─▶ Drafting ─▶ Escalation ─▶ Follow-up
          classify   assign      fetch KB docs     write reply   flag risky    schedule
          urgency/   team                          grounded      tickets       check-ins
          sentiment                                in KB
```

The drafted reply is then fact-checked against the retrieved knowledge-base
context (hallucination detection) before being shown to a human agent.

## Repository structure

| Folder                        | What it is                                             |
| ----------------------------- | ------------------------------------------------------ |
| [`backend/`](backend/)        | FastAPI API, LangGraph agents, RAG pipeline, MCP server |
| [`frontend/`](frontend/)      | Next.js dashboard UI                                   |
| [`docker-compose.yml`](docker-compose.yml) | One-command local deployment (API + UI + MCP) |

## Quick start

```bash
cp .env.example .env         # add your free Groq API key (console.groq.com/keys)
docker compose up --build
```

| Service    | URL                        |
| ---------- | -------------------------- |
| Web UI     | http://localhost:3000      |
| API docs   | http://localhost:8000/docs |
| MCP server | http://localhost:8001/mcp  |

No Docker? See [`backend/README.md`](backend/README.md) for local setup,
configuration, the MCP integration, deployment guides (Render / Vercel /
Fly.io), and troubleshooting.

## Highlights

- **Multi-agent orchestration** — six-agent LangGraph workflow with typed state
- **Grounded generation** — replies cite only knowledge-base content, verified
  by an LLM fact-checker
- **Provider-swappable LLM layer** — Groq (free tier), Claude API, or local
  Ollama via one env var
- **MCP server** — the whole pipeline is callable as a tool by any MCP client
  (Claude, Claude Code, other agents)
- **Production packaging** — slim Docker images (ONNX embeddings, no PyTorch),
  vector store baked at build time, configurable CORS
