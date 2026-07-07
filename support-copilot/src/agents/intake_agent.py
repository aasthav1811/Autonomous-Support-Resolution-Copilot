import json
import re
from src.utils.llm import get_llm
from src.config import CATEGORIES, URGENCY_LEVELS

INTAKE_PROMPT = """You are a support ticket triage classifier.

Classify the ticket into:
- category: one of {categories}
- urgency: one of {urgencies}
- sentiment: positive | neutral | negative | angry

Urgency definitions:
- low: general inquiry, no immediate action needed
- medium: issue affecting usage but not blocking
- high: blocking issue or repeated failure
- critical: financial loss, security issue, or very angry customer

Classification rules:
- "refund", "payment", "charged", "billing" → billing
- "crash", "error", "login", "bug" → technical
- "email", "account", "profile", "username" → account
- "order", "shipping", "delivery", "package" → shipping

Guidelines:
- Do NOT overestimate urgency
- Most tickets are medium unless clearly critical
- Only mark critical if money loss or extreme anger is present

Ticket Subject: {subject}
Ticket Body: {body}

Respond ONLY in JSON like:
{{"category": "...", "urgency": "...", "sentiment": "...", "confidence": 0.0}}"""

def _extract_json(text: str) -> dict:
    """Robust JSON extractor — handles Ollama's tendency to add extra text."""
    text = text.strip()

    # Try direct parse first
    try:
        return json.loads(text)
    except Exception:
        pass

    # Strip markdown code blocks
    text = re.sub(r"```(?:json)?", "", text).strip().rstrip("```").strip()
    try:
        return json.loads(text)
    except Exception:
        pass

    # Find first {...} block
    match = re.search(r"\{[^{}]+\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass

    # Fallback defaults (never crash the pipeline)
    return {"category": "general", "urgency": "medium", "sentiment": "neutral"}


def intake_agent(state):
    llm = get_llm(temperature=0)
    prompt = INTAKE_PROMPT.format(
        categories=", ".join(CATEGORIES),
        urgencies=", ".join(URGENCY_LEVELS),
        subject=state["subject"],
        body=state["body"],
    )
    response = llm.invoke(prompt).content
    parsed = _extract_json(response)

    confidence = parsed.get("confidence", 0.7)
    
    # Validate values — normalize to closest match
    category = parsed.get("category", "general").lower()
    if category not in CATEGORIES:
        category = "general"

    urgency = parsed.get("urgency", "medium").lower()
    if urgency not in URGENCY_LEVELS:
        urgency = "medium"

    sentiment = parsed.get("sentiment", "neutral").lower()
    if sentiment not in ["positive", "neutral", "negative", "angry"]:
        sentiment = "neutral"

    trace = state.get("agent_trace", []) + ["IntakeAgent"]
    return {
        "category": parsed["category"],
        "urgency": parsed["urgency"],
        "sentiment": parsed["sentiment"],
        "confidence": confidence,
        "agent_trace": trace,
    }
