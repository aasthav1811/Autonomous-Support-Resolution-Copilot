from langgraph.graph import StateGraph, END
from src.graph.state import TicketState
from src.agents.intake_agent import intake_agent
from src.agents.routing_agent import routing_agent
from src.agents.retrieval_agent import retrieval_agent
from src.agents.drafting_agent import drafting_agent
from src.agents.escalation_agent import escalation_agent
from src.agents.followup_agent import followup_agent


def build_workflow():
    graph = StateGraph(TicketState)

    graph.add_node("intake", intake_agent)
    graph.add_node("routing", routing_agent)
    graph.add_node("retrieval", retrieval_agent)
    graph.add_node("drafting", drafting_agent)
    graph.add_node("escalation", escalation_agent)
    graph.add_node("followup", followup_agent)

    graph.set_entry_point("intake")
    graph.add_edge("intake", "routing")
    graph.add_edge("routing", "retrieval")
    graph.add_edge("retrieval", "drafting")
    graph.add_edge("drafting", "escalation")
    graph.add_edge("escalation", "followup")
    graph.add_edge("followup", END)

    return graph.compile()


# Singleton — build once, reuse
_workflow = None


def get_workflow():
    global _workflow
    if _workflow is None:
        _workflow = build_workflow()
    return _workflow
