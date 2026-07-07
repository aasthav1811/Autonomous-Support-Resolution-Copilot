from src.utils.llm import get_llm

DRAFT_PROMPT = """You are a customer support agent. Write a reply to this support ticket.

TICKET:
Subject: {subject}
Message: {body}
Customer tone: {sentiment}
Category: {category}

KNOWLEDGE BASE (use ONLY this information, do not invent anything):
{context}

INSTRUCTIONS:
- Write a helpful, professional reply
- If the customer is angry or upset, start with a sincere apology
- Use information ONLY from the Knowledge Base above
- If the KB does not have enough info, say you are escalating to a specialist
- Keep the reply under 200 words
- Do NOT mention that you are an AI
- Do NOT add any preamble like "Here is my reply:" - just write the reply directly
- If the query is unclear or incomplete, ask a polite clarifying question instead of assuming details.
Reply:"""


def drafting_agent(state):
    llm = get_llm(temperature=0.3)
    context = "\n\n---\n\n".join(
        d["content"] for d in state.get("retrieved_docs", [])
    ) or "No relevant knowledge base articles found for this issue."

    prompt = DRAFT_PROMPT.format(
        subject=state["subject"],
        body=state["body"],
        sentiment=state.get("sentiment", "neutral"),
        category=state.get("category", "general"),
        context=context,
    )
    draft = llm.invoke(prompt).content.strip()

    # Remove common Llama preambles if present
    for prefix in ["Here is", "Here's", "Reply:", "Response:", "Dear"]:
        if draft.lower().startswith(prefix.lower()):
            break  # fine, keep it

    trace = state.get("agent_trace", []) + ["DraftingAgent"]
    return {"draft_response": draft, "agent_trace": trace}
