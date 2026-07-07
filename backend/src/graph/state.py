from typing import TypedDict, List, Optional
from typing_extensions import NotRequired


class TicketState(TypedDict):
    # Input
    ticket_id: str
    customer_email: str
    subject: str
    body: str

    # Intake Agent output
    category: NotRequired[str]
    urgency: NotRequired[str]
    sentiment: NotRequired[str]
    confidence: NotRequired[float]
    
    # Routing Agent output
    assigned_team: NotRequired[str]

    # Retrieval Agent output
    retrieved_docs: NotRequired[List[dict]]

    # Drafting Agent output
    draft_response: NotRequired[str]

    # Escalation Agent output
    needs_escalation: NotRequired[bool]
    escalation_reason: NotRequired[str]

    # Follow-up Agent output
    followup_required: NotRequired[bool]

    # Observability
    agent_trace: NotRequired[List[str]]
