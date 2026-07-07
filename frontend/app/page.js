'use client';
import { useState } from 'react';

// Inlined at build time — set NEXT_PUBLIC_API_URL when building for production
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const PRESETS = {
  "😤 Angry billing complaint": {
    subject: "CHARGED TWICE — REFUND NOW",
    body: "Your system charged my card THREE times for one subscription! This is fraud. I want all my money back TODAY or I'm disputing with my bank.",
  },
  "🔧 App crash report": {
    subject: "App crashes every time I open it",
    body: "The app crashes within 10 seconds of opening on my iPhone 14 (latest iOS). I've tried reinstalling. Please fix ASAP, I'm losing work.",
  },
  "❓ Can't login": {
    subject: "Cannot login to my account",
    body: "I keep getting 'invalid credentials' but I'm sure my password is correct. Please help.",
  },
  "📦 Lost package": {
    subject: "Order hasn't arrived — tracking stuck",
    body: "Order #12345 was placed 10 days ago. Tracking hasn't updated in 7 days. Where is my package?",
  },
  "✨ Feature request": {
    subject: "Dark mode request",
    body: "Would really love a dark mode option in the app. Any plans?",
  },
};

const URGENCY_COLORS = {
  low: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
  medium: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
  high: 'bg-orange-500/10 text-orange-400 border-orange-500/20',
  critical: 'bg-red-500/10 text-red-400 border-red-500/20',
};

const SENTIMENT_COLORS = {
  positive: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
  neutral: 'bg-zinc-500/10 text-zinc-400 border-zinc-500/20',
  negative: 'bg-orange-500/10 text-orange-400 border-orange-500/20',
  angry: 'bg-red-500/10 text-red-400 border-red-500/20',
};

function Badge({ label, colorClass }) {
  return (
    <span className={`px-3 py-1 rounded-full text-xs font-semibold border uppercase tracking-wider ${colorClass}`}>
      {label}
    </span>
  );
}

function AgentStep({ name, index, active }) {
  const icons = ['🔍', '🗺️', '📚', '✍️', '⚠️', '📅'];
  return (
    <div className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all border ${
      active
        ? 'bg-violet-500/10 text-violet-300 border-violet-500/20'
        : 'bg-zinc-800/50 text-zinc-500 border-zinc-700/50'
    }`}>
      <span>{icons[index] || '🤖'}</span>
      <span>{name}</span>
    </div>
  );
}

export default function Home() {
  const [tab, setTab] = useState('ticket');
  const [form, setForm] = useState({
    ticket_id: 'T999',
    customer_email: 'user@example.com',
    subject: '',
    body: '',
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [toast, setToast] = useState('');
  const [batchResults, setBatchResults] = useState([]);
  const [batchLoading, setBatchLoading] = useState(false);

  function showToast(msg) {
    setToast(msg);
    setTimeout(() => setToast(''), 3000);
  }

  function applyPreset(key) {
    if (key === 'Custom') return;
    const preset = PRESETS[key];
    if (preset) setForm(f => ({ ...f, ...preset }));
    setResult(null);
  }

  async function runWorkflow() {
    if (!form.subject || !form.body) { setError('Please fill in subject and body.'); return; }
    setError(''); setLoading(true); setResult(null);
    try {
      const res = await fetch(`${API_URL}/process_ticket`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();
      setResult(data);
    } catch (e) {
      const msg = e instanceof Error ? e.message : 'Unknown error';
      setError(msg.includes('fetch')
        ? `❌ Cannot reach the API at ${API_URL}. Is the backend running?`
        : msg);
    } finally {
      setLoading(false);
    }
  }

  async function runBatch() {
    setBatchLoading(true);
    setBatchResults([]);
    const tickets = [
      { ticket_id: 'T001', customer_email: 'john@example.com', subject: 'Cannot login', body: "Invalid credentials error but password is correct." },
      { ticket_id: 'T002', customer_email: 'sarah@example.com', subject: 'Refund request URGENT', body: "Charged twice for subscription! Refund immediately." },
      { ticket_id: 'T003', customer_email: 'mike@example.com', subject: 'Where is my package', body: "Order #12345 supposed to arrive 5 days ago. Tracking not updating." },
      { ticket_id: 'T004', customer_email: 'lisa@example.com', subject: 'Feature request', body: "Would love dark mode. Any plans?" },
      { ticket_id: 'T005', customer_email: 'raj@example.com', subject: 'App crashes constantly', body: "Crashes within 10 seconds. iPhone 14, latest iOS." },
    ];
    const results = [];
    for (const t of tickets) {
      try {
        const res = await fetch(`${API_URL}/process_ticket`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(t),
        });
        const data = await res.json();
        results.push(data);
        setBatchResults([...results]);
      } catch (e) {
        console.error('Batch error:', e);
      }
    }
    setBatchLoading(false);
  }

  const tabs = [
    { key: 'ticket', label: '🎫 Process Ticket' },
    { key: 'batch', label: '📊 Batch Demo' },
    { key: 'arch', label: '🏗️ Architecture' },
  ];

  const archAgents = [
    { icon: '🔍', name: 'Intake Agent', desc: 'LLM classifies category, urgency, sentiment', uses: 'LLM' },
    { icon: '🗺️', name: 'Routing Agent', desc: 'Assigns ticket to correct team', uses: 'Rules' },
    { icon: '📚', name: 'Retrieval Agent', desc: 'ChromaDB vector search over knowledge base', uses: 'RAG' },
    { icon: '✍️', name: 'Drafting Agent', desc: 'LLM writes grounded, empathetic reply', uses: 'LLM' },
    { icon: '⚠️', name: 'Escalation Agent', desc: 'Flags angry / urgent / unknown tickets', uses: 'Rules' },
    { icon: '📅', name: 'Follow-up Agent', desc: 'Schedules follow-up for risky tickets', uses: 'Rules' },
  ];

  const stackItems = [
    { label: 'LLM', value: 'Ollama + Llama 3.2 (local)', tag: 'Free' },
    { label: 'Orchestration', value: 'LangGraph StateGraph', tag: 'Open Source' },
    { label: 'Vector DB', value: 'ChromaDB (local)', tag: 'Free' },
    { label: 'Embeddings', value: 'all-MiniLM-L6-v2 (local)', tag: 'Free' },
    { label: 'Backend', value: 'FastAPI + Python', tag: 'Open Source' },
    { label: 'Frontend', value: 'Next.js + Tailwind CSS', tag: 'Open Source' },
  ];

  const keyMetrics = [
    { label: 'Cost per ticket', value: '$0.00', sub: '100% local' },
    { label: 'Agents with LLM', value: '2 / 6', sub: 'rest use rules' },
    { label: 'KB retrieval', value: 'Top-3', sub: 'category-filtered' },
    { label: 'Hallu. detection', value: 'LLM-judge', sub: 'every response' },
  ];

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100" style={{ fontFamily: "'DM Sans', sans-serif" }}>

      {/* Subtle grid */}
      <div className="fixed inset-0 pointer-events-none"
        style={{ backgroundImage: 'linear-gradient(rgba(124,109,250,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(124,109,250,0.03) 1px, transparent 1px)', backgroundSize: '48px 48px' }} />

      {/* Toast */}
      {toast && (
        <div className="fixed top-6 right-6 z-50 bg-violet-600 text-white px-5 py-3 rounded-xl shadow-2xl text-sm font-medium">
          {toast}
        </div>
      )}

      <div className="relative max-w-6xl mx-auto px-6 py-10">

        {/* Header */}
        <div className="mb-10">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-violet-600 flex items-center justify-center text-xl">🤖</div>
            <h1 className="text-3xl font-bold tracking-tight text-zinc-100">Support Copilot</h1>
            <span className="ml-2 px-3 py-1 bg-violet-500/10 border border-violet-500/20 rounded-full text-xs text-violet-400 font-medium">
              Ollama · Free 
            </span>
          </div>
          <p className="text-zinc-500 text-sm">Multi-agent AI for autonomous ticket resolution · LangGraph + RAG</p>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 mb-8 bg-zinc-900 p-1 rounded-xl border border-zinc-800 w-fit">
          {tabs.map(({ key, label }) => (
            <button key={key} onClick={() => setTab(key)}
              className={`px-5 py-2 rounded-lg text-sm font-medium transition-all ${
                tab === key ? 'bg-violet-600 text-white shadow-lg' : 'text-zinc-500 hover:text-zinc-200 hover:bg-zinc-800'
              }`}>
              {label}
            </button>
          ))}
        </div>

        {/* ── TICKET TAB ── */}
        {tab === 'ticket' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

            {/* Form */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 space-y-4">
              <h2 className="text-base font-semibold text-zinc-100">Submit a Ticket</h2>

              <div>
                <label className="text-xs text-zinc-500 font-medium uppercase tracking-wider mb-1.5 block">Load Sample</label>
                <select onChange={e => applyPreset(e.target.value)}
                  className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-2.5 text-sm text-zinc-200 focus:outline-none focus:border-violet-500 transition-colors">
                  <option>Custom</option>
                  {Object.keys(PRESETS).map(k => <option key={k}>{k}</option>)}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs text-zinc-500 font-medium uppercase tracking-wider mb-1.5 block">Ticket ID</label>
                  <input value={form.ticket_id} onChange={e => setForm(f => ({ ...f, ticket_id: e.target.value }))}
                    className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-2.5 text-sm text-zinc-200 focus:outline-none focus:border-violet-500 transition-colors" />
                </div>
                <div>
                  <label className="text-xs text-zinc-500 font-medium uppercase tracking-wider mb-1.5 block">Email</label>
                  <input value={form.customer_email} onChange={e => setForm(f => ({ ...f, customer_email: e.target.value }))}
                    className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-2.5 text-sm text-zinc-200 focus:outline-none focus:border-violet-500 transition-colors" />
                </div>
              </div>

              <div>
                <label className="text-xs text-zinc-500 font-medium uppercase tracking-wider mb-1.5 block">Subject</label>
                <input value={form.subject} onChange={e => setForm(f => ({ ...f, subject: e.target.value }))}
                  placeholder="Briefly describe the issue..."
                  className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-2.5 text-sm text-zinc-200 focus:outline-none focus:border-violet-500 transition-colors placeholder:text-zinc-600" />
              </div>

              <div>
                <label className="text-xs text-zinc-500 font-medium uppercase tracking-wider mb-1.5 block">Message</label>
                <textarea value={form.body} onChange={e => setForm(f => ({ ...f, body: e.target.value }))}
                  rows={5} placeholder="Full ticket message..."
                  className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-2.5 text-sm text-zinc-200 focus:outline-none focus:border-violet-500 transition-colors placeholder:text-zinc-600 resize-none" />
              </div>

              {error && (
                <p className="text-red-400 text-sm bg-red-500/10 border border-red-500/20 rounded-xl px-4 py-3">{error}</p>
              )}

              <button onClick={runWorkflow} disabled={loading}
                className="w-full bg-violet-600 hover:bg-violet-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-xl transition-all text-sm">
                {loading ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Agents working... (~15–30s)
                  </span>
                ) : '🚀 Run Multi-Agent Workflow'}
              </button>
              <p className="text-xs text-zinc-600 text-center">First run ~30s while Llama loads into memory</p>
            </div>

            {/* Results */}
            <div className="space-y-4">
              {!result && !loading && (
                <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl flex flex-col items-center justify-center text-center p-10 min-h-96">
                  <div className="text-5xl mb-4 opacity-20">🤖</div>
                  <p className="text-zinc-600 text-sm">Submit a ticket to see the 6-agent pipeline run</p>
                </div>
              )}

              {loading && (
                <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl flex flex-col items-center justify-center text-center p-10 min-h-96">
                  <div className="flex flex-wrap gap-2 justify-center mb-8">
                    {['Intake','Routing','Retrieval','Drafting','Escalation','FollowUp'].map((name, i) => (
                      <AgentStep key={name} name={name} index={i} active={true} />
                    ))}
                  </div>
                  <div className="w-8 h-8 border-2 border-violet-500/30 border-t-violet-500 rounded-full animate-spin mb-4" />
                  <p className="text-zinc-400 text-sm font-medium">Running 6-agent pipeline...</p>
                </div>
              )}

              {result && (
                <div className="space-y-4">
                  <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5">
                    <p className="text-xs text-zinc-500 uppercase tracking-wider mb-3 font-medium">Classification</p>
                    <div className="flex flex-wrap gap-2 mb-3">
                      <Badge label={result.category} colorClass="bg-violet-500/10 text-violet-400 border-violet-500/20" />
                      <Badge label={result.urgency} colorClass={URGENCY_COLORS[result.urgency] || URGENCY_COLORS.medium} />
                      <Badge label={result.sentiment} colorClass={SENTIMENT_COLORS[result.sentiment] || SENTIMENT_COLORS.neutral} />
                    </div>
                    <p className="text-sm text-zinc-400">
                      📩 Routed to: <span className="font-semibold text-zinc-100">{result.assigned_team}</span>
                    </p>
                  </div>

                  {result.needs_escalation ? (
                    <div className="bg-red-500/10 border border-red-500/20 rounded-2xl p-4 text-sm text-red-400">
                      ⚠️ <span className="font-semibold">Escalation needed:</span> {result.escalation_reason}
                      {result.followup_required && <span className="ml-2 text-amber-400">· 📅 Follow-up scheduled</span>}
                    </div>
                  ) : (
                    <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-2xl p-4 text-sm text-emerald-400">
                      ✅ No escalation needed · Auto-resolvable ticket
                    </div>
                  )}

                  <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5">
                    <p className="text-xs text-zinc-500 uppercase tracking-wider mb-3 font-medium">✉️ Draft Response</p>
                    <textarea defaultValue={result.draft_response} rows={7}
                      className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-sm text-zinc-200 focus:outline-none focus:border-violet-500 resize-none transition-colors" />
                    <div className="flex gap-2 mt-3">
                      <button onClick={() => showToast('✅ Response approved!')}
                        className="flex-1 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium py-2 rounded-xl transition-all">
                        ✅ Approve
                      </button>
                      <button onClick={() => showToast('✏️ Saved!')}
                        className="flex-1 bg-zinc-700 hover:bg-zinc-600 text-white text-sm font-medium py-2 rounded-xl transition-all">
                        ✏️ Edit
                      </button>
                      <button onClick={() => showToast('🚫 Flagged')}
                        className="flex-1 bg-red-900/30 hover:bg-red-800/50 text-red-400 text-sm font-medium py-2 rounded-xl transition-all border border-red-800/30">
                        🚫 Reject
                      </button>
                    </div>
                  </div>

                  <div className={`rounded-2xl p-4 text-sm border ${
                    result.hallucination_check?.hallucinated
                      ? 'bg-red-500/10 border-red-500/20 text-red-400'
                      : 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
                  }`}>
                    {result.hallucination_check?.hallucinated ? '⚠️ Possible hallucination: ' : '🧪 ✅ Grounded — '}
                    <span className="opacity-70">{result.hallucination_check?.explanation}</span>
                  </div>

                  <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5">
                    <p className="text-xs text-zinc-500 uppercase tracking-wider mb-3 font-medium">🔍 Agent Trace</p>
                    <div className="flex flex-wrap gap-2">
                      {(result.agent_trace || []).map((agent, i) => (
                        <AgentStep key={i} name={agent.replace('Agent', '')} index={i} active={true} />
                      ))}
                    </div>
                  </div>

                  <details className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5">
                    <summary className="text-xs text-zinc-500 uppercase tracking-wider font-medium cursor-pointer hover:text-zinc-300 transition-colors">
                      📚 Retrieved KB Docs ({result.retrieved_docs?.length || 0})
                    </summary>
                    <div className="mt-4 space-y-3">
                      {(result.retrieved_docs || []).map((d, i) => (
                        <div key={i} className="bg-zinc-800 rounded-xl p-3 border border-zinc-700">
                          <p className="text-xs text-violet-400 font-medium mb-1">{d.metadata?.category}</p>
                          <p className="text-xs text-zinc-400 leading-relaxed">{d.content.slice(0, 300)}...</p>
                        </div>
                      ))}
                    </div>
                  </details>
                </div>
              )}
            </div>
          </div>
        )}

        {/* ── BATCH TAB ── */}
        {tab === 'batch' && (
          <div className="space-y-6">
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
              <h2 className="text-base font-semibold mb-2">Batch Processing Demo</h2>
              <p className="text-sm text-zinc-500 mb-5">Runs all 5 sample tickets through the full pipeline.</p>
              <button onClick={runBatch} disabled={batchLoading}
                className="bg-violet-600 hover:bg-violet-500 disabled:opacity-50 text-white font-semibold px-6 py-2.5 rounded-xl transition-all text-sm">
                {batchLoading ? (
                  <span className="flex items-center gap-2">
                    <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Processing... ({batchResults.length}/5)
                  </span>
                ) : '▶️ Run All Sample Tickets'}
              </button>
            </div>

            {batchResults.length > 0 && (
              <div className="bg-zinc-900 border border-zinc-800 rounded-2xl overflow-hidden">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-zinc-800">
                      {['Ticket','Subject','Category','Urgency','Sentiment','Team','Escalate'].map(h => (
                        <th key={h} className="text-left px-4 py-3 text-xs text-zinc-500 uppercase tracking-wider font-medium">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {batchResults.map((r, i) => (
                      <tr key={i} className="border-b border-zinc-800/50 hover:bg-zinc-800/40 transition-colors">
                        <td className="px-4 py-3 text-violet-400 font-mono text-xs">{r.ticket_id}</td>
                        <td className="px-4 py-3 text-zinc-300 max-w-40 truncate">{r.subject}</td>
                        <td className="px-4 py-3"><Badge label={r.category || '...'} colorClass="bg-violet-500/10 text-violet-400 border-violet-500/20" /></td>
                        <td className="px-4 py-3"><Badge label={r.urgency || '...'} colorClass={URGENCY_COLORS[r.urgency] || URGENCY_COLORS.medium} /></td>
                        <td className="px-4 py-3"><Badge label={r.sentiment || '...'} colorClass={SENTIMENT_COLORS[r.sentiment] || SENTIMENT_COLORS.neutral} /></td>
                        <td className="px-4 py-3 text-zinc-500 text-xs">{r.assigned_team}</td>
                        <td className="px-4 py-3">{r.needs_escalation ? <span className="text-red-400">🔴 Yes</span> : <span className="text-emerald-400">✅ No</span>}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* ── ARCHITECTURE TAB ── */}
        {tab === 'arch' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
              <h2 className="text-base font-semibold mb-5">6-Agent Pipeline</h2>
              <div className="space-y-2">
                {archAgents.map((a, i) => (
                  <div key={i}>
                    <div className="flex items-start gap-3 p-3 bg-zinc-800/60 rounded-xl border border-zinc-700/40">
                      <span className="text-xl mt-0.5">{a.icon}</span>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-0.5">
                          <p className="text-sm font-medium text-zinc-200">{a.name}</p>
                          <span className={`text-xs px-2 py-0.5 rounded-full font-medium border ${
                            a.uses === 'LLM' ? 'bg-violet-500/10 text-violet-400 border-violet-500/20'
                            : a.uses === 'RAG' ? 'bg-teal-500/10 text-teal-400 border-teal-500/20'
                            : 'bg-zinc-700/60 text-zinc-400 border-zinc-600/40'
                          }`}>{a.uses}</span>
                        </div>
                        <p className="text-xs text-zinc-500">{a.desc}</p>
                      </div>
                    </div>
                    {i < 5 && <div className="flex justify-center my-1"><div className="w-px h-4 bg-zinc-700" /></div>}
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-4">
              <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
                <h2 className="text-base font-semibold mb-4">Tech Stack</h2>
                <div className="space-y-3">
                  {stackItems.map(row => (
                    <div key={row.label} className="flex items-center justify-between py-2 border-b border-zinc-800 last:border-0">
                      <span className="text-xs text-zinc-500 uppercase tracking-wider font-medium w-28">{row.label}</span>
                      <span className="text-sm text-zinc-200 flex-1">{row.value}</span>
                      <span className="text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-full">{row.tag}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
                <h2 className="text-base font-semibold mb-4">Key Metrics</h2>
                <div className="grid grid-cols-2 gap-3">
                  {keyMetrics.map(m => (
                    <div key={m.label} className="bg-zinc-800 rounded-xl p-4 border border-zinc-700">
                      <p className="text-2xl font-bold text-violet-400 mb-1">{m.value}</p>
                      <p className="text-xs font-medium text-zinc-200">{m.label}</p>
                      <p className="text-xs text-zinc-500">{m.sub}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
