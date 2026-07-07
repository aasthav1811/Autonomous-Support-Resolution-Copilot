import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.graph.workflow import get_workflow
from src.evaluation.evaluator import check_hallucination

st.set_page_config(
    page_title="Support Copilot",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
    color: white;
}

/* Remove Streamlit menu/footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Glassmorphism cards */
.glass {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}

.metric-card {
    background: rgba(255,255,255,0.07);
    padding: 1rem;
    border-radius: 20px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
}

.big-title {
    font-size: 3rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0.2rem;
}

.subtitle {
    color: #cbd5e1;
    font-size: 1rem;
    margin-bottom: 2rem;
}

.section-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: white;
    margin-bottom: 1rem;
}

.stTextInput input,
.stTextArea textarea {
    background-color: rgba(255,255,255,0.06) !important;
    color: white !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

.stButton > button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 14px;
    border: none;
    padding: 0.7rem 1.4rem;
    font-weight: 600;
    transition: 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(99,102,241,0.4);
}

div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 1rem;
    border-radius: 20px;
}

.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 🧠 Support Copilot")
    st.caption("Enterprise AI Support Dashboard")

    st.markdown("---")

    st.metric("AI Status", "Online")
    st.metric("Model", "Llama 3.2")
    st.metric("Pipeline", "6 Agents")

    st.markdown("---")

    st.write("### Features")
    st.write("✅ Ticket Classification")
    st.write("✅ AI Response Drafting")
    st.write("✅ Knowledge Base Retrieval")
    st.write("✅ Escalation Detection")
    st.write("✅ Analytics Dashboard")

# =========================
# HEADER
# =========================
st.markdown('<div class="big-title">Support Copilot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered enterprise support operations dashboard</div>', unsafe_allow_html=True)

# =========================
# TABS
# =========================
tab1, tab2 = st.tabs(["🎫 Ticket Processing", "📊 Analytics"])

# =====================================================
# TAB 1
# =====================================================
with tab1:

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Submit Support Ticket</div>', unsafe_allow_html=True)

        tid = st.text_input("Ticket ID", "T999")
        email = st.text_input("Customer Email", "user@example.com")
        subject = st.text_input("Subject", "Cannot login to my account")

        body = st.text_area(
            "Ticket Description",
            "Hi, I keep getting an invalid credentials error when I try to log in. Please help.",
            height=180
        )

        run = st.button("🚀 Process Ticket")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if run:
            with st.spinner("AI agents processing request..."):
                wf = get_workflow()

                result = wf.invoke({
                    "ticket_id": tid,
                    "customer_email": email,
                    "subject": subject,
                    "body": body,
                    "agent_trace": [],
                })

                ctx = "\n".join(d["content"] for d in result.get("retrieved_docs", []))
                hallu = check_hallucination(result.get("draft_response", ""), ctx)

            st.markdown('<div class="glass">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">AI Processing Results</div>', unsafe_allow_html=True)

            m1, m2, m3, m4 = st.columns(4)

            with m1:
                st.metric("Category", result.get("category", "?"))

            with m2:
                st.metric("Urgency", result.get("urgency", "?"))

            with m3:
                st.metric("Sentiment", result.get("sentiment", "?"))

            with m4:
                confidence = round(result.get("confidence", 0.8) * 100)
                st.metric("Confidence", f"{confidence}%")

            st.markdown("---")

            if result.get("needs_escalation"):
                st.error(f"⚠ Escalation Required: {result.get('escalation_reason')}")
            else:
                st.success("✅ Ticket resolved without escalation")

            st.info(f"Assigned Team: {result.get('assigned_team')}")

            st.markdown("### ✉️ Draft Response")

            st.text_area(
                "Generated Response",
                result.get("draft_response", ""),
                height=260
            )

            c1, c2 = st.columns(2)

            with c1:
                st.button("✅ Approve Response")

            with c2:
                st.button("✏️ Edit Response")

            with st.expander("📚 Retrieved Knowledge Base Context"):
                for i, d in enumerate(result.get("retrieved_docs", [])):
                    st.markdown(f"### Document {i+1}")
                    st.caption(d['metadata'].get('category'))
                    st.write(d["content"][:500])

            with st.expander("🛡 Response Validation"):
                if hallu.get("hallucinated"):
                    st.error(hallu.get("explanation"))
                else:
                    st.success("Response grounded in knowledge base")

            with st.expander("⚙ System Trace"):
                st.write(" → ".join(result.get("agent_trace", [])))

            st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# TAB 2
# =====================================================
with tab2:

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Operational Analytics</div>', unsafe_allow_html=True)

    if st.button("📊 Run Batch Analysis"):

        df = pd.read_csv("data/tickets.csv")
        wf = get_workflow()

        results = []

        prog = st.progress(0)

        for i, row in df.iterrows():
            r = wf.invoke({
                "ticket_id": row["ticket_id"],
                "customer_email": row["customer_email"],
                "subject": row["subject"],
                "body": row["body"],
                "agent_trace": [],
            })

            results.append({
                "ticket_id": r["ticket_id"],
                "category": r.get("category"),
                "urgency": r.get("urgency"),
                "team": r.get("assigned_team"),
                "escalate": r.get("needs_escalation"),
            })

            prog.progress((i + 1) / len(df))

        rdf = pd.DataFrame(results)

        total = len(rdf)
        escalated = rdf["escalate"].sum()

        c1, c2, c3 = st.columns(3)

        c1.metric("Tickets Processed", total)
        c2.metric("Escalations", escalated)
        c3.metric("Automation Rate", f"{round((1-escalated/total)*100)}%")

        st.markdown("---")

        st.dataframe(rdf, use_container_width=True)

        g1, g2 = st.columns(2)

        with g1:
            fig = px.pie(
                rdf,
                names="category",
                title="Ticket Categories"
            )
            st.plotly_chart(fig, use_container_width=True)

        with g2:
            fig2 = px.bar(
                rdf.groupby("urgency").size().reset_index(name="count"),
                x="urgency",
                y="count",
                title="Urgency Distribution"
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

