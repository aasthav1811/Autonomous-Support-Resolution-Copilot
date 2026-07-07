from src.config import TEAM_ROUTING


def routing_agent(state):
    category = state.get("category", "general")
    team = TEAM_ROUTING.get(category, "Tier 1 Support")
    trace = state.get("agent_trace", []) + ["RoutingAgent"]
    return {"assigned_team": team, "agent_trace": trace}
