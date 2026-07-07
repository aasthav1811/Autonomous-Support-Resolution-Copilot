"""MCP server exposing the Support Copilot pipeline as a tool.

Run locally:      python api/mcp_server.py
Endpoint:         http://localhost:8001/mcp  (Streamable HTTP transport)

Any MCP client (Claude, Claude Code, other agents) can connect to this URL
and call the `process_ticket` tool.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP
from src.graph.workflow import get_workflow
from src.evaluation.evaluator import check_hallucination

mcp = FastMCP(
    "support-copilot",
    host=os.getenv("MCP_HOST", "0.0.0.0"),
    port=int(os.getenv("MCP_PORT", "8001")),
)


@mcp.tool()
def process_ticket(ticket_id: str, customer_email: str, subject: str, body: str) -> dict:
    """Run a customer support ticket through the multi-agent pipeline
    (intake → routing → RAG retrieval → drafting → escalation → follow-up)
    and return the classification, routing decision, drafted reply, and a
    hallucination check of the draft against the knowledge base."""
    workflow = get_workflow()
    result = workflow.invoke({
        "ticket_id": ticket_id,
        "customer_email": customer_email,
        "subject": subject,
        "body": body,
        "agent_trace": [],
    })
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
        "hallucination_check": hallu,
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
