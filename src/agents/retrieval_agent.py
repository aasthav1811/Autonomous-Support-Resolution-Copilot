from src.rag.retriever import KBRetriever


def retrieval_agent(state):
    retriever = KBRetriever()
    query = f"{state['subject']} {state['body']}"
    docs = retriever.retrieve(query, k=3, category=state.get("category"))
    trace = state.get("agent_trace", []) + ["RetrievalAgent"]
    return {"retrieved_docs": docs, "agent_trace": trace}
