import sys
import json
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.append(str(SRC))

from gridskill_multi_agent import GridSkillOrchestratorAgent
from gridskill_multi_agent_v2 import GridSkillAdvancedOrchestrator
from gridskill_multi_agent_v3 import GridSkillGroundedOrchestrator


st.set_page_config(
    page_title="GridSkill IQ | Enterprise AI Workforce Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 12% 8%, rgba(59,130,246,0.25), transparent 30%),
        radial-gradient(circle at 88% 5%, rgba(14,165,233,0.25), transparent 28%),
        linear-gradient(180deg, #020617 0%, #0f172a 34%, #f8fafc 34%, #eef2ff 100%);
}

.block-container {
    padding-top: 1.1rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #0f172a 60%, #111827 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] * {
    color: #f8fafc;
}

.header-shell {
    background: rgba(15,23,42,0.82);
    backdrop-filter: blur(22px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 24px;
    padding: 14px 20px;
    margin-bottom: 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 18px 60px rgba(0,0,0,0.32);
}

.brand-wrap {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo-box {
    width: 42px;
    height: 42px;
    border-radius: 14px;
    background: linear-gradient(135deg, #facc15, #38bdf8);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #020617;
    font-weight: 950;
    font-size: 22px;
    box-shadow: 0 14px 30px rgba(56,189,248,0.28);
}

.brand-title {
    color: white;
    font-weight: 950;
    font-size: 23px;
    letter-spacing: -0.5px;
}

.brand-sub {
    color: #94a3b8;
    font-size: 12px;
    margin-top: -2px;
}

.nav-pill {
    display: inline-block;
    color: #cbd5e1;
    font-size: 13px;
    font-weight: 700;
    padding: 9px 12px;
    border-radius: 999px;
    margin-left: 6px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
}

.nav-pill-active {
    display: inline-block;
    color: #020617;
    font-size: 13px;
    font-weight: 900;
    padding: 9px 13px;
    border-radius: 999px;
    margin-left: 6px;
    background: #facc15;
}

.hero-grid {
    display: grid;
    grid-template-columns: 1.25fr 0.75fr;
    gap: 22px;
    margin-bottom: 22px;
}

.hero-main {
    background:
        linear-gradient(135deg, rgba(30,64,175,0.92), rgba(15,23,42,0.98)),
        radial-gradient(circle at top right, rgba(56,189,248,0.45), transparent 35%);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 34px;
    padding: 42px;
    min-height: 390px;
    color: white;
    box-shadow: 0 30px 90px rgba(2,6,23,0.46);
    position: relative;
    overflow: hidden;
}

.hero-main:before {
    content: "";
    position: absolute;
    width: 360px;
    height: 360px;
    border-radius: 999px;
    right: -120px;
    top: -140px;
    background: rgba(56,189,248,0.20);
    filter: blur(2px);
}

.hero-eyebrow {
    display: inline-flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 18px;
}

.hero-tag {
    display: inline-block;
    padding: 8px 13px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
    color: #dbeafe;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.18);
}

.hero-title {
    font-size: 58px;
    line-height: 1;
    letter-spacing: -2.2px;
    font-weight: 950;
    max-width: 960px;
    margin-bottom: 18px;
    position: relative;
    z-index: 2;
}

.hero-highlight {
    color: #facc15;
}

.hero-copy {
    color: #dbeafe;
    font-size: 18px;
    line-height: 1.65;
    max-width: 940px;
    position: relative;
    z-index: 2;
}

.hero-actions {
    margin-top: 28px;
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    position: relative;
    z-index: 2;
}

.btn-yellow {
    display: inline-block;
    background: #facc15;
    color: #020617;
    font-weight: 950;
    padding: 13px 18px;
    border-radius: 999px;
    box-shadow: 0 16px 34px rgba(250,204,21,0.18);
}

.btn-glass {
    display: inline-block;
    background: rgba(255,255,255,0.08);
    color: white;
    font-weight: 800;
    padding: 13px 18px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.16);
}

.hero-side {
    background: rgba(15,23,42,0.88);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 34px;
    padding: 28px;
    color: white;
    box-shadow: 0 30px 90px rgba(2,6,23,0.36);
}

.live-dot {
    width: 9px;
    height: 9px;
    background: #22c55e;
    display: inline-block;
    border-radius: 999px;
    margin-right: 8px;
    box-shadow: 0 0 20px rgba(34,197,94,0.75);
}

.side-title {
    font-size: 20px;
    font-weight: 950;
    margin-bottom: 14px;
}

.pipeline-step {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    padding: 12px 14px;
    border-radius: 16px;
    margin-bottom: 10px;
    color: #e2e8f0;
    font-size: 14px;
}

.kpi-card {
    background: rgba(255,255,255,0.92);
    border: 1px solid rgba(226,232,240,0.95);
    box-shadow: 0 18px 50px rgba(15,23,42,0.10);
    border-radius: 24px;
    padding: 22px;
}

.kpi-label {
    color: #64748b;
    font-size: 12px;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.75px;
}

.kpi-value {
    color: #020617;
    font-size: 35px;
    font-weight: 950;
    letter-spacing: -1.2px;
    margin-top: 4px;
}

.kpi-note {
    color: #64748b;
    font-size: 13px;
    margin-top: 6px;
}

.section-title {
    color: #020617;
    font-size: 32px;
    font-weight: 950;
    letter-spacing: -1px;
    margin-top: 28px;
    margin-bottom: 5px;
}

.section-copy {
    color: #64748b;
    font-size: 15px;
    margin-bottom: 18px;
}

.lux-card {
    background: white;
    border-radius: 26px;
    padding: 26px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 18px 50px rgba(15,23,42,0.08);
    min-height: 184px;
}

.lux-card h3 {
    color: #020617;
    font-size: 20px;
    font-weight: 950;
    margin-bottom: 9px;
}

.lux-card p {
    color: #475569;
    font-size: 14.5px;
    line-height: 1.58;
}

.agent-tile {
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 24px;
    padding: 22px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 14px 38px rgba(15,23,42,0.075);
    min-height: 168px;
}

.agent-icon {
    width: 44px;
    height: 44px;
    border-radius: 15px;
    background: linear-gradient(135deg, #1d4ed8, #38bdf8);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 950;
    margin-bottom: 12px;
}

.agent-title {
    color: #020617;
    font-weight: 950;
    font-size: 16px;
    margin-bottom: 7px;
}

.agent-desc {
    color: #64748b;
    font-size: 13.5px;
    line-height: 1.5;
}

.profile-card {
    background:
        linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #e2e8f0;
    border-radius: 28px;
    padding: 26px;
    box-shadow: 0 18px 50px rgba(15,23,42,0.08);
}

.profile-title {
    font-size: 22px;
    font-weight: 950;
    color: #020617;
    margin-bottom: 12px;
}

.profile-line {
    color: #475569;
    font-size: 14.5px;
    margin-bottom: 8px;
}

.badge-ready {
    background: #dcfce7;
    color: #166534;
    padding: 6px 12px;
    border-radius: 999px;
    font-weight: 950;
    font-size: 12px;
}

.badge-high {
    background: #fee2e2;
    color: #991b1b;
    padding: 6px 12px;
    border-radius: 999px;
    font-weight: 950;
    font-size: 12px;
}

.badge-mid {
    background: #fef3c7;
    color: #92400e;
    padding: 6px 12px;
    border-radius: 999px;
    font-weight: 950;
    font-size: 12px;
}

.command-box {
    background: #020617;
    color: #e2e8f0;
    border-radius: 24px;
    padding: 22px;
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 22px 55px rgba(2,6,23,0.22);
}

.footer {
    color: #64748b;
    text-align: center;
    font-size: 13px;
    padding: 28px 0 10px 0;
}
</style>
""",
    unsafe_allow_html=True
)


@st.cache_data
def load_data():
    learners = pd.read_csv(ROOT / "data" / "synthetic" / "learners.csv")
    work = pd.read_csv(ROOT / "data" / "synthetic" / "work_signals.csv")
    return learners, work


def readiness_badge(status):
    if status == "Ready":
        return '<span class="badge-ready">READY</span>'
    if status == "High Risk":
        return '<span class="badge-high">HIGH RISK</span>'
    return f'<span class="badge-mid">{status.upper()}</span>'


learners_df, work_df = load_data()
basic_agent = GridSkillOrchestratorAgent()
advanced_agent = GridSkillAdvancedOrchestrator()
grounded_agent = GridSkillGroundedOrchestrator()


with st.sidebar:
    st.markdown("## ⚡ GridSkill IQ")
    st.caption("Enterprise AI Workforce Intelligence")
    st.markdown("---")
    st.markdown("### Product Stack")
    st.write("🧠 Orchestrated specialist agents")
    st.write("📚 Grounded synthetic knowledge")
    st.write("🗓️ Workload-aware planning")
    st.write("🧪 Readiness assessment")
    st.write("📊 Manager intelligence")
    st.write("🛡️ Safety critic")
    st.write("📡 Trace telemetry")
    st.write("✅ Evaluation report")
    st.markdown("---")
    st.markdown("### Challenge Alignment")
    st.write("**Track:** Reasoning Agents")
    st.write("**Theme:** Enterprise learning")
    st.write("**Data:** Synthetic only")
    st.write("**IQ:** Foundry / Work / Fabric")
    st.markdown("---")
    st.warning("Demo uses synthetic data only. No PII or confidential information.")


st.markdown(
    """
<div class="header-shell">
    <div class="brand-wrap">
        <div class="logo-box">⚡</div>
        <div>
            <div class="brand-title">GridSkill IQ</div>
            <div class="brand-sub">Enterprise AI Workforce Intelligence Platform</div>
        </div>
    </div>
    <div>
        <span class="nav-pill-active">Command Centre</span>
        <span class="nav-pill">Agents</span>
        <span class="nav-pill">Telemetry</span>
        <span class="nav-pill">Trust</span>
    </div>
</div>
""",
    unsafe_allow_html=True
)


st.markdown(
    """
<div class="hero-grid">
    <div class="hero-main">
        <div class="hero-eyebrow">
            <span class="hero-tag">Microsoft Agents League</span>
            <span class="hero-tag">Reasoning Agents</span>
            <span class="hero-tag">Multi-Agent Orchestration</span>
            <span class="hero-tag">Synthetic Data Only</span>
        </div>
        <div class="hero-title">
            The AI command centre for <span class="hero-highlight">energy workforce readiness</span>.
        </div>
        <div class="hero-copy">
            GridSkill IQ coordinates specialist AI agents to map role-based certifications,
            generate workload-aware study plans, assess readiness, surface manager-level risk,
            and validate outputs through a safety critic and trace telemetry layer.
        </div>
        <div class="hero-actions">
            <span class="btn-yellow">Run Intelligence Workflow</span>
            <span class="btn-glass">View Agent Telemetry</span>
        </div>
    </div>
    <div class="hero-side">
        <div class="side-title"><span class="live-dot"></span>Live Agent Pipeline</div>
        <div class="pipeline-step">01 · Orchestrator receives learner or manager request</div>
        <div class="pipeline-step">02 · Learning agent maps role to certification path</div>
        <div class="pipeline-step">03 · Study agent plans around workload capacity</div>
        <div class="pipeline-step">04 · Assessment agent evaluates readiness</div>
        <div class="pipeline-step">05 · Safety critic validates final response</div>
        <div class="pipeline-step">06 · Trace logger records evidence and confidence</div>
    </div>
</div>
""",
    unsafe_allow_html=True
)


total_learners = len(learners_df)
high_risk = int((learners_df["readiness_status"] == "High Risk").sum())
ready = int((learners_df["readiness_status"] == "Ready").sum())
avg_score = learners_df["practice_score_avg"].mean()

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f"""
<div class="kpi-card">
    <div class="kpi-label">Synthetic Learners</div>
    <div class="kpi-value">{total_learners}</div>
    <div class="kpi-note">Demo workforce profiles</div>
</div>
""",
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
<div class="kpi-card">
    <div class="kpi-label">High Risk Learners</div>
    <div class="kpi-value">{high_risk}</div>
    <div class="kpi-note">Need manager attention</div>
</div>
""",
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
<div class="kpi-card">
    <div class="kpi-label">Ready Learners</div>
    <div class="kpi-value">{ready}</div>
    <div class="kpi-note">Ready by readiness rules</div>
</div>
""",
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f"""
<div class="kpi-card">
    <div class="kpi-label">Average Practice Score</div>
    <div class="kpi-value">{avg_score:.1f}%</div>
    <div class="kpi-note">Across synthetic learners</div>
</div>
""",
        unsafe_allow_html=True
    )


st.markdown('<div class="section-title">Premium Agent Product Suite</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-copy">Designed like an enterprise AI platform: specialised agents, trust controls, evidence tracking and manager insight.</div>',
    unsafe_allow_html=True
)

p1, p2, p3 = st.columns(3)

with p1:
    st.markdown(
        """
<div class="lux-card">
    <h3>🧠 Agentic Intelligence</h3>
    <p>
    A coordinated multi-agent workflow decomposes the learning-readiness problem into
    specialised reasoning tasks instead of using one generic chatbot.
    </p>
</div>
""",
        unsafe_allow_html=True
    )

with p2:
    st.markdown(
        """
<div class="lux-card">
    <h3>🏢 Enterprise Context</h3>
    <p>
    Synthetic work signals simulate meeting load, focus hours, preferred learning slots,
    shift patterns and team-level readiness constraints.
    </p>
</div>
""",
        unsafe_allow_html=True
    )

with p3:
    st.markdown(
        """
<div class="lux-card">
    <h3>🛡️ Trust & Safety</h3>
    <p>
    Outputs include source tracking, confidence scoring, synthetic-data disclaimers,
    safety validation and trace logs for observability.
    </p>
</div>
""",
        unsafe_allow_html=True
    )


st.markdown('<div class="section-title">Agent Marketplace</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-copy">Six specialist agents operating through an orchestration layer.</div>',
    unsafe_allow_html=True
)

agent_rows = [
    ("01", "Learning Path Curator", "Maps role, certification, skill gap and approved learning content."),
    ("02", "Study Plan Generator", "Builds workload-aware plans using hours studied, meeting load and focus time."),
    ("03", "Engagement Agent", "Recommends reminder strategies that avoid disrupting operational work patterns."),
    ("04", "Assessment Agent", "Evaluates readiness and generates grounded practice questions."),
    ("05", "Manager Insights Agent", "Creates team-level readiness summaries and action recommendations."),
    ("06", "Safety Critic Agent", "Checks for privacy issues, unsupported claims and synthetic-data clarity."),
]

cols = st.columns(3)
for idx, item in enumerate(agent_rows):
    with cols[idx % 3]:
        st.markdown(
            f"""
<div class="agent-tile">
    <div class="agent-icon">{item[0]}</div>
    <div class="agent-title">{item[1]}</div>
    <div class="agent-desc">{item[2]}</div>
</div>
""",
            unsafe_allow_html=True
        )


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "⚡ Intelligence Console",
        "📊 Manager Centre",
        "📡 Trace Telemetry",
        "🧪 Evaluation & Safety",
        "🏗️ Architecture"
    ]
)


with tab1:
    st.markdown('<div class="section-title">Learner Intelligence Console</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Run a complete AI readiness workflow for a synthetic energy workforce learner.</div>',
        unsafe_allow_html=True
    )

    employee_id = st.selectbox(
        "Select synthetic employee",
        learners_df["employee_id"].tolist(),
        key="ultra_employee"
    )

    learner = learners_df[learners_df["employee_id"] == employee_id].iloc[0]
    work = work_df[work_df["employee_id"] == employee_id].iloc[0]

    role = learner["role"]
    team = learner["team_id"]
    cert = learner["target_certification"]
    skill_gap = learner["skill_gap"]
    score = learner["practice_score_avg"]
    hours = learner["hours_studied"]
    readiness = learner["readiness_status"]
    badge = readiness_badge(readiness)

    shift = work["shift_pattern"]
    meetings = work["meeting_hours_per_week"]
    focus = work["focus_hours_per_week"]
    slot = work["preferred_learning_slot"]

    left, right = st.columns([1, 1])

    with left:
        st.markdown(
            f"""
<div class="profile-card">
    <div class="profile-title">Learner Profile</div>
    <div class="profile-line"><b>Employee:</b> {employee_id}</div>
    <div class="profile-line"><b>Team:</b> {team}</div>
    <div class="profile-line"><b>Role:</b> {role}</div>
    <div class="profile-line"><b>Target Certification:</b> {cert}</div>
    <div class="profile-line"><b>Primary Skill Gap:</b> {skill_gap}</div>
    <div class="profile-line"><b>Practice Score:</b> {score}%</div>
    <div class="profile-line"><b>Hours Studied:</b> {hours}</div>
    <div class="profile-line"><b>Readiness:</b> {badge}</div>
</div>
""",
            unsafe_allow_html=True
        )

    with right:
        st.markdown(
            f"""
<div class="profile-card">
    <div class="profile-title">Work Context Intelligence</div>
    <div class="profile-line"><b>Shift Pattern:</b> {shift}</div>
    <div class="profile-line"><b>Meeting Load:</b> {meetings} hours/week</div>
    <div class="profile-line"><b>Focus Capacity:</b> {focus} hours/week</div>
    <div class="profile-line"><b>Preferred Learning Slot:</b> {slot}</div>
    <div class="profile-line"><b>Planning Mode:</b> Workload-aware</div>
    <div class="profile-line"><b>Safety Mode:</b> Synthetic data only</div>
</div>
""",
            unsafe_allow_html=True
        )

    st.markdown("### Run AI Workflow")

    run1, run2 = st.columns(2)

    with run1:
        if st.button("Run Standard Multi-Agent Workflow", use_container_width=True):
            response = basic_agent.learner_workflow(employee_id)
            st.text_area("Standard Workflow Output", response, height=520)

    with run2:
        if st.button("Run Advanced V2 Intelligence Workflow", use_container_width=True):
            response = advanced_agent.learner_workflow(employee_id)
            st.text_area("Advanced Intelligence Output", response, height=680)


with tab2:
    st.markdown('<div class="section-title">Manager Command Centre</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Team-level certification readiness view for synthetic workforce planning.</div>',
        unsafe_allow_html=True
    )

    team_summary = (
        learners_df.groupby(["team_id", "readiness_status"])
        .size()
        .reset_index(name="count")
    )

    pivot = team_summary.pivot(
        index="team_id",
        columns="readiness_status",
        values="count"
    ).fillna(0)

    st.dataframe(pivot, use_container_width=True)

    mleft, mright = st.columns([1, 1])

    with mleft:
        st.subheader("Synthetic Learner Portfolio")
        st.dataframe(learners_df, use_container_width=True, hide_index=True)

    with mright:
        st.subheader("Synthetic Work Signals")
        st.dataframe(work_df, use_container_width=True, hide_index=True)

    if st.button("Run Manager Intelligence Agent", use_container_width=True):
        response = advanced_agent.manager_workflow()
        st.text_area("Manager Intelligence Output", response, height=540)


with tab3:
    st.markdown('<div class="section-title">Trace Telemetry Console</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Observability layer showing agent sequence, sources, confidence and safety status.</div>',
        unsafe_allow_html=True
    )

    trace_path = ROOT / "reports" / "agent_trace_log.json"

    if trace_path.exists():
        trace = json.loads(trace_path.read_text(encoding="utf-8"))
        events_df = pd.DataFrame(trace.get("events", []))

        t1, t2, t3, t4 = st.columns(4)
        t1.metric("Trace ID", trace.get("run_id", "")[:8])
        t2.metric("Agent Events", trace.get("event_count", 0))
        t3.metric("Started", trace.get("started_at", "N/A"))
        t4.metric("Finished", trace.get("finished_at", "N/A"))

        st.subheader("Agent Event Timeline")
        st.dataframe(events_df, use_container_width=True, hide_index=True)

        with st.expander("Raw JSON Trace"):
            st.code(json.dumps(trace, indent=2), language="json")
    else:
        st.warning("No trace log found. Run Advanced V2 workflow first.")


with tab4:
    st.markdown('<div class="section-title">Evaluation & Responsible AI Centre</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Reliability, safety and evaluation evidence for hackathon judging.</div>',
        unsafe_allow_html=True
    )

    report_path = ROOT / "reports" / "evaluation_report.txt"

    if report_path.exists():
        report_text = report_path.read_text(encoding="utf-8")
        st.text_area("Evaluation Report", report_text, height=390)
    else:
        st.warning("Evaluation report not found. Run: python src\\evaluate_gridskill_iq.py")

    e1, e2, e3 = st.columns(3)

    with e1:
        st.markdown(
            """
<div class="lux-card">
    <h3>Privacy Guardrails</h3>
    <p>
    Uses fabricated identifiers only. No real employee, customer, confidential,
    credential or personally identifiable information is included.
    </p>
</div>
""",
            unsafe_allow_html=True
        )

    with e2:
        st.markdown(
            """
<div class="lux-card">
    <h3>Safety Validation</h3>
    <p>
    The Safety Critic Agent reviews outputs for unsupported claims,
    unsafe phrasing and synthetic-data disclaimer clarity.
    </p>
</div>
""",
            unsafe_allow_html=True
        )

    with e3:
        st.markdown(
            """
<div class="lux-card">
    <h3>Human Oversight</h3>
    <p>
    The system is designed for decision support only and does not automatically
    approve certification readiness or employment decisions.
    </p>
</div>
""",
            unsafe_allow_html=True
        )


with tab5:
    st.markdown('<div class="section-title">Architecture & Microsoft IQ Alignment</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">A production-style design narrative for the Reasoning Agents challenge.</div>',
        unsafe_allow_html=True
    )

    st.code(
        "User Request\n"
        "   ↓\n"
        "GridSkill Orchestrator Agent\n"
        "   ↓\n"
        "Planner / Router\n"
        "   ↓\n"
        "Learning Path Curator Agent\n"
        "Study Plan Generator Agent\n"
        "Engagement Agent\n"
        "Assessment Agent\n"
        "Manager Insights Agent\n"
        "   ↓\n"
        "Safety Critic Agent\n"
        "   ↓\n"
        "Trace Logger + Evaluation Report\n"
        "   ↓\n"
        "Final Grounded Response\n"
        "   ↓\n"
        "Premium Streamlit Product Interface",
        language="text"
    )

    iq1, iq2, iq3 = st.columns(3)

    with iq1:
        st.markdown(
            """
<div class="lux-card">
    <h3>Foundry IQ</h3>
    <p>
    Synthetic knowledge base documents serve as the grounding layer for role guidance,
    learning recommendations and assessment question generation.
    </p>
</div>
""",
            unsafe_allow_html=True
        )

    with iq2:
        st.markdown(
            """
<div class="lux-card">
    <h3>Work IQ</h3>
    <p>
    Synthetic work signals simulate meeting load, focus capacity, preferred learning slot
    and shift context for workload-aware planning.
    </p>
</div>
""",
            unsafe_allow_html=True
        )

    with iq3:
        st.markdown(
            """
<div class="lux-card">
    <h3>Fabric IQ</h3>
    <p>
    A semantic model connects learner, employee, team, role, certification, skill gap,
    study progress, practice score and readiness status.
    </p>
</div>
""",
            unsafe_allow_html=True
        )


st.markdown(
    """
<div class="footer">
    GridSkill IQ — Enterprise AI Workforce Intelligence | Synthetic Data Only | Microsoft Agents League Reasoning Agents Prototype
</div>
""",
    unsafe_allow_html=True
)