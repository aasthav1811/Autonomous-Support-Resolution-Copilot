import json
import re
from src.utils.llm import get_llm

HALLUCINATION_PROMPT = """You are a fact-checker. Check if the response contains any claims NOT supported by the context.

Context:
{context}

Response to check:
{response}

Respond ONLY with this JSON (no extra text):
{{"hallucinated": false, "explanation": "Response is grounded in context."}}

Or if there are unsupported claims:
{{"hallucinated": true, "explanation": "Brief explanation of what was invented."}}"""


def _extract_json(text: str) -> dict:
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    text = re.sub(r"```(?:json)?", "", text).strip().rstrip("```").strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    match = re.search(r"\{[^{}]+\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass
    return {"hallucinated": False, "explanation": "Could not parse evaluator response"}


def check_hallucination(response: str, context: str) -> dict:
    if not response or not context:
        return {"hallucinated": False, "explanation": "No context to check against"}

    llm = get_llm(temperature=0)
    prompt = HALLUCINATION_PROMPT.format(
        context=context[:2000],  # limit context for speed
        response=response,
    )
    out = llm.invoke(prompt).content
    return _extract_json(out)
