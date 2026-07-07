def followup_agent(state):
    followup = state.get("needs_escalation", False) or state.get("sentiment") == "angry"
    trace = state.get("agent_trace", []) + ["FollowUpAgent"]
    return {"followup_required": followup, "agent_trace": trace}
