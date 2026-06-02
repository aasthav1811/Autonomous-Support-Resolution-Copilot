# 🤖 Autonomous Support Resolution Copilot
### Multi-Agent AI · LangGraph · RAG · 100% Free with Ollama

---

## ✅ What's changed from the original?
The original used OpenAI (paid). This version uses **Ollama + Llama 3.2** — completely free, runs on your own computer, no API keys needed.

---

## 🚀 SETUP GUIDE (Follow in Order)

### STEP 1 — Install Ollama
Go to **https://ollama.com/download** and download Ollama for your OS (Windows/Mac/Linux).

After installing, open a terminal and run:
```bash
ollama serve
```
Leave this terminal open. Ollama needs to be running whenever you use the project.

---

### STEP 2 — Pull the Llama model
Open a **second terminal** and run:
```bash
ollama pull llama3.2
```
This downloads ~2GB (one-time only). Wait for it to finish.

To verify it worked:
```bash
ollama list
```
You should see `llama3.2` in the list.

---

### STEP 3 — Create the project folder structure
Open a terminal and run these commands one by one:
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

### STEP 4 — Copy all the code files
Copy every file from this project into the correct folders as shown in the structure below.

```
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
│   │   ├── __init__.py
│   │   ├── intake_agent.py
│   │   ├── routing_agent.py
│   │   ├── retrieval_agent.py
│   │   ├── drafting_agent.py
│   │   ├── escalation_agent.py
│   │   └── followup_agent.py
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── state.py
│   │   └── workflow.py
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── ingest.py
│   │   └── retriever.py
│   ├── evaluation/
│   │   ├── __init__.py
│   │   └── evaluator.py
│   └── utils/
│       ├── __init__.py
│       └── llm.py
├── api/
│   └── main.py
└── ui/
    └── app.py
```

---

### STEP 5 — Create a Python virtual environment
In your `support-copilot/` folder:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

---

### STEP 6 — Install dependencies
With venv activated:
```bash
pip install -r requirements.txt
```
This takes 3-5 minutes. Sentence-transformers is the largest download (~500MB, one-time).

---

### STEP 7 — Ingest the knowledge base (one-time setup)
```bash
python -m src.rag.ingest
```

Expected output:
```
Loading embedding model: all-MiniLM-L6-v2...
✅ Ingested 24 chunks from 4 files into ChromaDB.
```

If you see an error about `data/knowledge_base`, make sure you created the .md files in Step 4.

---

### STEP 8 — Run the Streamlit UI
Make sure Ollama is still running (`ollama serve` in background terminal).

```bash
streamlit run ui/app.py
```

Open your browser to: **http://localhost:8501**

The UI will show a green banner if Ollama is running correctly.

---

### STEP 9 — (Optional) Run the FastAPI backend
In a separate terminal:
```bash
uvicorn api.main:app --reload --port 8000
```

Then open: **http://localhost:8000/docs** to test the API interactively.

Or test with curl:
```bash
curl -X POST http://localhost:8000/process_ticket \
  -H "Content-Type: application/json" \
  -d '{"ticket_id":"T100","customer_email":"a@b.com","subject":"Refund please","body":"I was charged twice, I want my money back immediately!"}'
```

---

## ⚡ Every Time You Work on This Project

1. **Terminal 1:** `ollama serve` (keep open)
2. **Terminal 2 (in support-copilot folder, venv activated):** `streamlit run ui/app.py`

---

## 🔧 Troubleshooting

### "Connection refused" / Ollama not running
Run `ollama serve` in a terminal and keep it open.

### "Model not found" error
Run `ollama pull llama3.2` then try again.

### Response is very slow (>60s)
Normal for first run — Llama loads into memory. After that it's faster.
If consistently slow, try a lighter model:
```bash
ollama pull llama3.2:1b
```
Then in `.env` change: `OLLAMA_MODEL=llama3.2:1b`

### JSON parsing errors
The intake agent has fallback logic so it won't crash. But if you see wrong classifications, try:
```bash
ollama pull llama3.1
```
And change `.env` to `OLLAMA_MODEL=llama3.1`

### ChromaDB errors on re-ingest
Delete the chroma_db folder and run ingest again:
```bash
rm -rf chroma_db/
python -m src.rag.ingest
```

### `ModuleNotFoundError: No module named 'src'`
Make sure you're running commands from the `support-copilot/` root folder, not from inside a subfolder.

---

## 🆓 Why This is Completely Free

| Component | Original (Paid) | This Version (Free) |
|-----------|----------------|---------------------|
| LLM | OpenAI GPT-4o-mini ($) | Ollama Llama 3.2 (local) |
| Embeddings | Already free | all-MiniLM-L6-v2 (local) |
| Vector DB | Already free | ChromaDB (local) |
| Hosting | Cloud ($) | Your computer |
| Observability | LangSmith (optional) | LangSmith free tier |

**Total cost: $0.00** 

---

## 📊 Alternative Free Models (if Llama 3.2 is too slow)

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| `llama3.2:1b` | 1.3GB | ⚡⚡⚡ Fast | Good |
| `llama3.2` | 2.0GB | ⚡⚡ Medium | Better |
| `llama3.1` | 4.7GB | ⚡ Slow | Best |
| `mistral` | 4.1GB | ⚡ Slow | Very Good |
| `phi3` | 2.3GB | ⚡⚡ Medium | Good |

Change model in `.env`: `OLLAMA_MODEL=phi3`

---

## 🏗️ Architecture

```
Ticket In → IntakeAgent (LLM) → RoutingAgent (rules) → RetrievalAgent (RAG)
         → DraftingAgent (LLM) → EscalationAgent (rules) → FollowUpAgent (rules)
         → Human Approval → Send
```

Only 2 of 6 agents use the LLM — making this fast and resource-efficient.

---

## 📈 Skills Demonstrated
- ✅ Multi-agent orchestration (LangGraph)
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Local LLM deployment (Ollama)
- ✅ Hallucination detection (LLM-as-judge)
- ✅ Human-in-the-loop design
- ✅ Vector databases (ChromaDB)
- ✅ REST API (FastAPI)
- ✅ Interactive UI (Streamlit)
