# 🤖 Customer Support Resolution Copilot

### Multi-Agent AI · LangGraph · RAG · Ollama + Qwen2.5-Coder

---

## 🚀 Setup Guide

Follow the steps below in order.

---

## Step 1 — Install Ollama

Download and install Ollama for your operating system:

[Ollama Download Page](https://ollama.com/download?utm_source=chatgpt.com)

After installation, start Ollama:

```bash
ollama serve
```

Leave this terminal open. Ollama must be running whenever you use the project.

---

## Step 2 — Pull the Model

Open a second terminal and run:

```bash
ollama pull qwen2.5-coder:7b
```

This is a one-time download of approximately 4.7 GB.

Verify installation:

```bash
ollama list
```

Expected output:

```text
NAME
qwen2.5-coder:7b
```

---

## Step 3 — Create the Project Structure

```bash
mkdir support-copilot
cd support-copilot

mkdir -p data/knowledge_base
mkdir -p src/agents
mkdir -p src/graph
mkdir -p src/rag
mkdir -p src/evaluation
mkdir -p src/utils
mkdir -p api
mkdir -p ui
mkdir -p notebooks
```

---

## Step 4 — Copy Project Files

Copy all project files into the following structure:

```text
support-copilot/
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── data/
│   ├── tickets.csv
│   └── knowledge_base/
│       ├── billing_faq.md
│       ├── technical_faq.md
│       ├── account_faq.md
│       └── shipping_faq.md
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── agents/
│   │   ├── intake_agent.py
│   │   ├── routing_agent.py
│   │   ├── retrieval_agent.py
│   │   ├── drafting_agent.py
│   │   ├── escalation_agent.py
│   │   └── followup_agent.py
│   ├── graph/
│   │   ├── state.py
│   │   └── workflow.py
│   ├── rag/
│   │   ├── ingest.py
│   │   └── retriever.py
│   ├── evaluation/
│   │   └── evaluator.py
│   └── utils/
│       └── llm.py
├── api/
│   └── main.py
└── ui/
    └── app.py
```

---

## Step 5 — Create a Python Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3.11 -m venv venv
source venv/bin/activate
```

You should see:

```text
(venv)
```

at the beginning of your terminal prompt.

---

## Step 6 — Install Dependencies

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

Installation may take several minutes because PyTorch and Sentence Transformers are large dependencies.

---

## Step 7 — Configure Ollama

Create a `.env` file in the project root:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:7b
```

---

## Step 8 — Ingest the Knowledge Base (One-Time Setup)

```bash
python -m src.rag.ingest
```

Expected output:

```text
Loading embedding model: all-MiniLM-L6-v2...
Ingested knowledge base into ChromaDB.
```

If you encounter a knowledge base error, ensure the markdown files exist inside:

```text
data/knowledge_base/
```

---

## Step 9 — Run the Streamlit Interface

Make sure Ollama is still running.

```bash
streamlit run ui/app.py
```

Open:

```text
http://localhost:8501
```

The application should launch in your browser.

---

## Step 10 — Run the FastAPI Backend (Optional)

In a separate terminal:

```bash
uvicorn api.main:app --reload --port 8000
```

Open:

```text
http://localhost:8000/docs
```

to test the API using Swagger UI.

Example API request:

```bash
curl -X POST http://localhost:8000/process_ticket \
  -H "Content-Type: application/json" \
  -d '{"ticket_id":"T100","customer_email":"a@b.com","subject":"Refund please","body":"I was charged twice and would like a refund."}'
```

---

# Daily Workflow

Whenever you work on the project:

### Terminal 1

```bash
ollama serve
```

Keep this terminal running.

### Terminal 2

```bash
source venv/bin/activate
streamlit run ui/app.py
```

Or:

```bash
source venv/bin/activate
uvicorn api.main:app --reload --port 8000
```

if using the API backend.

---

# Troubleshooting

## Ollama Connection Refused

Ensure Ollama is running:

```bash
ollama serve
```

Verify connectivity:

```bash
curl http://localhost:11434/api/tags
```

---

## Model Not Found

Check installed models:

```bash
ollama list
```

If the model is missing:

```bash
ollama pull qwen2.5-coder:7b
```

Verify your `.env` file contains:

```env
OLLAMA_MODEL=qwen2.5-coder:7b
```

Restart the application after making changes.

---

## Slow First Response

The first request may take longer because Ollama loads the model into memory.

Subsequent requests are significantly faster.

---

## ChromaDB Re-ingestion Issues

Delete the local database and ingest again:

```bash
rm -rf chroma_db/
python -m src.rag.ingest
```

---

## ModuleNotFoundError: No module named 'src'

Make sure you are running commands from the project root:

```text
support-copilot/
```

and not from a subfolder.

---

# Why This Project Is Cost-Free

| Component           | Technology                |
| ------------------- | ------------------------- |
| LLM                 | Ollama + Qwen2.5-Coder 7B |
| Embeddings          | all-MiniLM-L6-v2          |
| Vector Database     | ChromaDB                  |
| Agent Orchestration | LangGraph                 |
| Backend API         | FastAPI                   |
| Frontend UI         | Streamlit                 |
| Hosting             | Local Machine             |

**Total Cost: $0**

---

# Alternative Models

| Model              | Size   | Recommended Use            |
| ------------------ | ------ | -------------------------- |
| `qwen2.5-coder:7b` | ~4.7GB | Recommended default        |
| `qwen2.5:7b`       | ~4.4GB | General-purpose assistant  |
| `mistral`          | ~4.1GB | Fast general-purpose model |
| `phi3`             | ~2.3GB | Lightweight option         |

To switch models:

```env
OLLAMA_MODEL=<model-name>
```

Then restart the application.

---

# Architecture

```text
Ticket Input
     │
     ▼
Intake Agent
     │
     ▼
Routing Agent
     │
     ▼
Retrieval Agent (RAG)
     │
     ▼
Drafting Agent
     │
     ▼
Escalation Agent
     │
     ▼
Follow-Up Agent
     │
     ▼
Human Review
     │
     ▼
Final Response
```

Only the Intake and Drafting agents rely on the LLM, reducing latency and computational overhead.

---

# Skills Demonstrated

* Multi-Agent Orchestration with LangGraph
* Retrieval-Augmented Generation (RAG)
* Local LLM Deployment with Ollama
* Vector Databases with ChromaDB
* FastAPI Backend Development
* Streamlit Application Development
* Human-in-the-Loop AI Systems
* Prompt Engineering
* Knowledge Retrieval Pipelines
* AI-Powered Customer Support Automation
