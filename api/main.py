import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.graph.workflow import get_workflow
from src.evaluation.evaluator import check_hallucination

app = FastAPI(title="Support Copilot API")

# ← ADD THIS — allows Next.js (port 3000) to talk to FastAPI (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TicketRequest(BaseModel):
    ticket_id: str
    customer_email: str
    subject: str
    body: str

@app.get("/")
def root():
    return {"status": "ok", "service": "Support Copilot", "llm": "Ollama (local, free)"}

@app.get("/health")
def health():
    import requests
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        models = [m["name"] for m in r.json().get("models", [])]
        return {"ollama": "running", "available_models": models}
    except Exception as e:
        return {"ollama": "unreachable", "error": str(e)}

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