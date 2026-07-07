def escalation_agent(state):
    urgency = state.get("urgency", "low")
    sentiment = state.get("sentiment", "neutral")
    docs = state.get("retrieved_docs", [])
    confidence = state.get("confidence", 1.0)

    needs_escalation = False
    reason = []

    if urgency in ["high", "critical"]:
        needs_escalation = True
        reason.append(f"High urgency: {urgency}")

    if sentiment == "angry":
        needs_escalation = True
        reason.append("Customer is angry")

    if confidence < 0.5:
        needs_escalation = True
        reason.append("Low classification confidence")

    if len(docs) == 0 and urgency in ["high", "critical"]:
        needs_escalation = True
        reason.append("No KB match + high urgency")

    trace = state.get("agent_trace", []) + ["EscalationAgent"]
    return {
        "needs_escalation": needs_escalation,
        "escalation_reason": "; ".join(reason) if reason else "None",
        "agent_trace": trace,
    }
