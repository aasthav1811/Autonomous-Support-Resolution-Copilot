import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.config import CORS_ORIGINS, LLM_PROVIDER, GROQ_MODEL, ANTHROPIC_MODEL, OLLAMA_BASE_URL, OLLAMA_MODEL
from src.graph.workflow import get_workflow
from src.evaluation.evaluator import check_hallucination

app = FastAPI(title="Support Copilot API")

# Origins allowed to call this API from a browser (set CORS_ORIGINS in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TicketRequest(BaseModel):
    ticket_id: str
    customer_email: str
    subject: str
    body: str

_MODELS = {"groq": GROQ_MODEL, "anthropic": ANTHROPIC_MODEL, "ollama": f"{OLLAMA_MODEL} (Ollama, local)"}

@app.get("/")
def root():
    llm = _MODELS.get(LLM_PROVIDER, "unknown")
    return {"status": "ok", "service": "Support Copilot", "provider": LLM_PROVIDER, "llm": llm}

@app.get("/health")
def health():
    if LLM_PROVIDER in ("groq", "anthropic"):
        key_var = "GROQ_API_KEY" if LLM_PROVIDER == "groq" else "ANTHROPIC_API_KEY"
        status = "configured" if os.getenv(key_var) else f"MISSING — set {key_var}"
        return {"provider": LLM_PROVIDER, "model": _MODELS[LLM_PROVIDER], "api_key": status}

    import requests
    try:
        r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        models = [m["name"] for m in r.json().get("models", [])]
        return {"provider": "ollama", "ollama": "running", "available_models": models}
    except Exception as e:
        return {"provider": "ollama", "ollama": "unreachable", "error": str(e)}

@app.post("/process_ticket")
def process_ticket(req: TicketRequest):
    workflow = get_workflow()
    initial_state = {
        "ticket_id": req.ticket_id,
        "customer_email": req.customer_email,
        "subject": req.subject,
        "body": req.body,
        "agent_trace": [],
    }
    result = workflow.invoke(initial_state)
    context = "\n".join(d["content"] for d in result.get("retrieved_docs", []))
    hallu = check_hallucination(result.get("draft_response", ""), context)

    return {
        "ticket_id": result["ticket_id"],
        "category": result.get("category"),
        "urgency": result.get("urgency"),
        "sentiment": result.get("sentiment"),
        "assigned_team": result.get("assigned_team"),
        "draft_response": result.get("draft_response"),
        "needs_escalation": result.get("needs_escalation"),
        "escalation_reason": result.get("escalation_reason"),
        "followup_required": result.get("followup_required"),
        "agent_trace": result.get("agent_trace"),
        "retrieved_docs": result.get("retrieved_docs"),
        "hallucination_check": hallu,
    }
