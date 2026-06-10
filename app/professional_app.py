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


st.set_page_config(
    page_title="GridSkill IQ",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
    }

    .hero {
        padding: 32px;
        border-radius: 18px;
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #2563eb 100%);
        color: white;
        margin-bottom: 24px;
    }

    .hero h1 {
        font-size: 46px;
        margin-bottom: 8px;
    }

    .hero p {
        font-size: 18px;
        color: #dbeafe;
        max-width: 950px;
    }

    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background-color: rgba(255,255,255,0.14);
        margin-right: 8px;
        font-size: 13px;
        border: 1px solid rgba(255,255,255,0.25);
    }

    .card {
        background: white;
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(15,23,42,0.08);
        border: 1px solid #e5e7eb;
        min-height: 150px;
    }

    .card h3 {
        color: #0f172a;
        margin-bottom: 8px;
    }

    .card p {
        color: #475569;
        font-size: 15px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 800;
        color: #0f172a;
        margin-top: 20px;
        margin-bottom: 8px;
    }

    .small-muted {
        color: #64748b;
        font-size: 14px;
    }

    .risk-high {
        color: #991b1b;
        font-weight: 700;
    }

    .risk-ready {
        color: #166534;
        font-weight: 700;
    }

    .footer {
        padding: 18px;
        color: #64748b;
        text-align: center;
        font-size: 13px;
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


learners_df, work_df = load_data()
basic_agent = GridSkillOrchestratorAgent()
advanced_agent = GridSkillAdvancedOrchestrator()


with st.sidebar:
    st.title("⚡ GridSkill IQ")
    st.caption("Reasoning Agents Hackathon Prototype")

    st.markdown("---")
    st.subheader("System Modules")
    st.write("✅ Multi-agent orchestration")
    st.write("✅ Synthetic data")
    st.write("✅ Knowledge grounding")
    st.write("✅ Readiness assessment")
    st.write("✅ Safety critic")
    st.write("✅ Trace logging")
    st.write("✅ Evaluation report")

    st.markdown("---")
    st.subheader("Microsoft IQ Alignment")
    st.write("**Foundry IQ:** synthetic knowledge grounding")
    st.write("**Work IQ:** synthetic work-context signals")
    st.write("**Fabric IQ:** semantic learner-role-certification model")

    st.markdown("---")
    st.warning("Synthetic demo data only. No real employee, customer, confidential, or PII data is used.")


st.markdown(
    """
    <div class="hero">
        <span class="badge">Microsoft Agents League</span>
        <span class="badge">Reasoning Agents</span>
        <span class="badge">Synthetic Data Only</span>
        <span class="badge">Responsible AI</span>
        <h1>GridSkill IQ</h1>
        <p>
        A professional multi-agent reasoning system for UK energy workforce certification readiness,
        workload-aware study planning, grounded assessment, manager-level insights, and safety-reviewed AI outputs.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


total_learners = len(learners_df)
high_risk_count = int((learners_df["readiness_status"] == "High Risk").sum())
ready_count = int((learners_df["readiness_status"] == "Ready").sum())
avg_score = learners_df["practice_score_avg"].mean()

m1, m2, m3, m4 = st.columns(4)

m1.metric("Synthetic Learners", total_learners)
m2.metric("High Risk Learners", high_risk_count)
m3.metric("Ready Learners", ready_count)
m4.metric("Average Practice Score", f"{avg_score:.1f}%")


st.markdown('<div class="section-title">Executive Overview</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="card">
            <h3>Multi-Agent Reasoning</h3>
            <p>
            GridSkill IQ coordinates specialised agents for learning path curation,
            study planning, engagement, assessment, manager insights, and safety validation.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div class="card">
            <h3>Workload-Aware Planning</h3>
            <p>
            The system uses synthetic meeting load, focus hours, shift pattern, and preferred learning slot
            to recommend realistic study plans.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        """
        <div class="card">
            <h3>Responsible AI Controls</h3>
            <p>
            Every response includes synthetic-data positioning, source tracking, safety validation,
            and decision-support limitations.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Learner Intelligence",
        "Manager Command Centre",
        "Advanced Trace",
        "Data & Evaluation",
        "Architecture"
    ]
)


with tab1:
    st.markdown('<div class="section-title">Learner Certification Readiness Agent</div>', unsafe_allow_html=True)
    st.caption("Run a full multi-agent workflow for a synthetic employee.")

    employee_id = st.selectbox(
        "Select synthetic employee",
        learners_df["employee_id"].tolist(),
        key="learner_select"
    )

    learner_row = learners_df[learners_df["employee_id"] == employee_id].iloc[0]

    a, b, c, d = st.columns(4)
    a.metric("Role", learner_row["role"])
    b.metric("Certification", learner_row["target_certification"])
    c.metric("Practice Score", f"{learner_row['practice_score_avg']}%")
    d.metric("Readiness", learner_row["readiness_status"])

    st.dataframe(
        learners_df[learners_df["employee_id"] == employee_id],
        use_container_width=True,
        hide_index=True
    )

    col_run1, col_run2 = st.columns(2)

    with col_run1:
        if st.button("Run Standard Multi-Agent Workflow", use_container_width=True):
            response = basic_agent.learner_workflow(employee_id)
            st.text_area("Standard Agent Output", response, height=550)

    with col_run2:
        if st.button("Run Advanced V2 Workflow", use_container_width=True):
            response = advanced_agent.learner_workflow(employee_id)
            st.text_area("Advanced Agent Output", response, height=650)


with tab2:
    st.markdown('<div class="section-title">Manager Command Centre</div>', unsafe_allow_html=True)
    st.caption("Team-level certification readiness view using synthetic learner data.")

    summary = (
        learners_df.groupby(["team_id", "readiness_status"])
        .size()
        .reset_index(name="count")
    )

    st.dataframe(summary, use_container_width=True, hide_index=True)

    left, right = st.columns([1, 1])

    with left:
        st.subheader("Synthetic Learner Portfolio")
        st.dataframe(learners_df, use_container_width=True, hide_index=True)

    with right:
        st.subheader("Synthetic Work Signals")
        st.dataframe(work_df, use_container_width=True, hide_index=True)

    if st.button("Run Manager Insights Agent", use_container_width=True):
        response = advanced_agent.manager_workflow()
        st.text_area("Manager Agent Output", response, height=520)


with tab3:
    st.markdown('<div class="section-title">Advanced Agent Trace & Telemetry</div>', unsafe_allow_html=True)
    st.caption("Shows structured trace logging, confidence scoring, source tracking, and safety validation.")

    trace_path = ROOT / "reports" / "agent_trace_log.json"

    st.info("Run an Advanced V2 workflow first, then refresh this tab to see the latest JSON trace.")

    if trace_path.exists():
        trace = json.loads(trace_path.read_text(encoding="utf-8"))

        t1, t2, t3 = st.columns(3)
        t1.metric("Trace Run ID", trace.get("run_id", "")[:8])
        t2.metric("Agent Events", trace.get("event_count", 0))
        t3.metric("Finished At", trace.get("finished_at", "N/A"))

        events_df = pd.DataFrame(trace.get("events", []))

        if not events_df.empty:
            st.subheader("Agent Event Timeline")
            st.dataframe(events_df, use_container_width=True, hide_index=True)

        with st.expander("View raw JSON trace"):
            st.code(json.dumps(trace, indent=2), language="json")
    else:
        st.warning("No trace log found yet. Run the Advanced V2 workflow first.")


with tab4:
    st.markdown('<div class="section-title">Data, Evaluation & Safety</div>', unsafe_allow_html=True)

    st.subheader("Evaluation Report")
    report_path = ROOT / "reports" / "evaluation_report.txt"

    if report_path.exists():
        report_text = report_path.read_text(encoding="utf-8")
        st.text_area("Evaluation Report", report_text, height=400)
    else:
        st.warning("Evaluation report not found. Run: python src\\evaluate_gridskill_iq.py")

    st.subheader("Responsible AI Controls")
    st.write("✅ Synthetic data only")
    st.write("✅ No real employee or customer data")
    st.write("✅ No confidential information")
    st.write("✅ Safety Critic Agent")
    st.write("✅ Source tracking")
    st.write("✅ Human oversight recommended")
    st.write("✅ Decision support only, not automatic certification approval")


with tab5:
    st.markdown('<div class="section-title">System Architecture</div>', unsafe_allow_html=True)

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
        "Professional Streamlit Frontend",
        language="text"
    )

    st.subheader("Foundry IQ Alignment")
    st.write(
        "Synthetic knowledge base documents act as the grounding layer. "
        "In a full Microsoft Foundry implementation, these documents can be indexed for grounded retrieval and citations."
    )

    st.subheader("Work IQ Alignment")
    st.write(
        "Synthetic work signals such as meeting hours, focus hours, preferred learning slot, and shift pattern "
        "represent work-context intelligence for scheduling and engagement."
    )

    st.subheader("Fabric IQ Alignment")
    st.write(
        "The project models semantic relationships between learner, employee, team, role, certification, skill gap, "
        "study hours, practice score, and readiness status."
    )


st.markdown(
    """
    <div class="footer">
        GridSkill IQ — Multi-Agent Reasoning System | Synthetic Data Only | Built for Microsoft Agents League Hackathon
    </div>
    """,
    unsafe_allow_html=True
)