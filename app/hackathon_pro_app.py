
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
DATA_DIR = ROOT / "data" / "synthetic"
REPORTS_DIR = ROOT / "reports"
DOCS_DIR = ROOT / "docs"

sys.path.insert(0, str(SRC_DIR))

from gridskill_multi_agent import GridSkillOrchestratorAgent
from gridskill_multi_agent_v2 import GridSkillAdvancedOrchestrator
from gridskill_multi_agent_v3 import GridSkillGroundedOrchestrator


st.set_page_config(
    page_title="GridSkill IQ",
    page_icon="⚡",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .subtitle {
        font-size: 20px;
        color: #6b7280;
        margin-top: 4px;
    }
    .card {
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        background: #ffffff;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        margin-bottom: 16px;
    }
    .metric-card {
        padding: 18px;
        border-radius: 14px;
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        text-align: center;
    }
    .small-label {
        color: #6b7280;
        font-size: 14px;
    }
    .big-number {
        font-size: 30px;
        font-weight: 800;
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%);
        color: #e5e7eb;
    }

    [data-testid="stSidebar"] {
        background: #020617;
        border-right: 1px solid rgba(148,163,184,0.25);
    }

    .hero-pro {
        padding: 36px;
        border-radius: 28px;
        background:
            radial-gradient(circle at top left, rgba(37,99,235,0.38), transparent 28%),
            radial-gradient(circle at bottom right, rgba(14,165,233,0.24), transparent 30%),
            linear-gradient(135deg, rgba(15,23,42,0.96), rgba(30,41,59,0.88));
        border: 1px solid rgba(148,163,184,0.28);
        box-shadow: 0 25px 80px rgba(0,0,0,0.42);
        margin-bottom: 24px;
    }

    .hero-pro-title {
        font-size: 56px;
        font-weight: 900;
        letter-spacing: -1.8px;
        color: #f8fafc;
        margin-bottom: 12px;
    }

    .hero-pro-subtitle {
        font-size: 20px;
        line-height: 1.55;
        color: #cbd5e1;
        max-width: 1050px;
    }

    .pill-pro {
        display: inline-block;
        padding: 8px 13px;
        border-radius: 999px;
        border: 1px solid rgba(125,211,252,0.38);
        background: rgba(14,165,233,0.14);
        color: #bae6fd;
        font-size: 13px;
        font-weight: 800;
        margin-right: 8px;
        margin-bottom: 12px;
    }

    .card, .metric-card {
        background: rgba(15,23,42,0.78) !important;
        border: 1px solid rgba(148,163,184,0.25) !important;
        box-shadow: 0 16px 45px rgba(0,0,0,0.25) !important;
        color: #e5e7eb !important;
    }

    .small-label {
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 800;
    }

    .big-number {
        color: #f8fafc !important;
        font-size: 36px !important;
        font-weight: 900 !important;
    }

    .stButton > button {
        border-radius: 14px;
        height: 3.1rem;
        font-weight: 850;
        border: 1px solid rgba(125,211,252,0.42);
        background: linear-gradient(135deg, #2563eb, #0891b2);
        color: white;
        box-shadow: 0 12px 32px rgba(37,99,235,0.26);
    }

    .stButton > button:hover {
        filter: brightness(1.10);
        border: 1px solid rgba(186,230,253,0.9);
        transform: translateY(-1px);
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(15,23,42,0.75);
        border-radius: 14px;
        border: 1px solid rgba(148,163,184,0.18);
        color: #cbd5e1;
        font-weight: 800;
        padding: 12px 18px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(37,99,235,0.60), rgba(8,145,178,0.50));
        color: #ffffff;
        border: 1px solid rgba(125,211,252,0.38);
    }

    textarea {
        background-color: #020617 !important;
        color: #e5e7eb !important;
        border: 1px solid rgba(148,163,184,0.35) !important;
        border-radius: 16px !important;
        font-family: Consolas, monospace !important;
        font-size: 13px !important;
    }

    h1, h2, h3, h4, p, li, label {
        color: #e5e7eb !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_data
def load_learners():
    path = DATA_DIR / "learners.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def get_agents():
    basic = GridSkillOrchestratorAgent()
    advanced = GridSkillAdvancedOrchestrator()
    grounded = GridSkillGroundedOrchestrator()
    return basic, advanced, grounded


learners = load_learners()
basic_agent, advanced_agent, grounded_agent = get_agents()

st.markdown(
    '''
    <div class="hero-pro">
        <span class="pill-pro">Microsoft Agents League</span>
        <span class="pill-pro">Reasoning Agents</span>
        <span class="pill-pro">V3 Grounded Retrieval</span>
        <span class="pill-pro">Synthetic Data Only</span>
        <div class="hero-pro-title">GridSkill IQ</div>
        <div class="hero-pro-subtitle">
            A professional multi-agent reasoning prototype for UK energy workforce certification readiness.
            It combines grounded knowledge retrieval, specialist agent orchestration, confidence scoring,
            trace telemetry, manager insights and responsible AI safety validation.
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)

st.success(
    "Demo mode: synthetic data only. No real employee, customer, confidential or personally identifiable data is used."
)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Overview",
        "Learner Intelligence",
        "Manager Centre",
        "Trace Telemetry",
        "Evaluation & Safety",
        "Architecture"
    ]
)

with tab1:
    st.markdown("## Project Overview")

    if learners.empty:
        st.error("Learner data not found. Run: python src\\create_synthetic_data.py")
    else:
        total_learners = len(learners)
        high_risk = len(learners[learners["readiness_status"].str.contains("High Risk|At Risk", case=False, na=False)])
        ready = len(learners[learners["readiness_status"].str.contains("Ready|Nearly Ready", case=False, na=False)])
        avg_score = round(learners["practice_score_avg"].mean(), 1)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(f'<div class="metric-card"><div class="small-label">Synthetic Learners</div><div class="big-number">{total_learners}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><div class="small-label">At Risk Learners</div><div class="big-number">{high_risk}</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><div class="small-label">Ready / Nearly Ready</div><div class="big-number">{ready}</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="metric-card"><div class="small-label">Average Practice Score</div><div class="big-number">{avg_score}</div></div>', unsafe_allow_html=True)

    st.markdown("### What this project does")
    st.markdown(
        """
        GridSkill IQ helps a synthetic energy organisation understand learner certification readiness.

        It uses:
        - Standard multi-agent workflow
        - Advanced V2 workflow with confidence scoring and trace logging
        - Grounded V3 workflow with knowledge retrieval and evidence sources
        - Manager-level readiness insights
        - Safety Critic Agent validation
        - Evaluation and telemetry reporting
        """
    )

    if st.button("Run Quick Grounded V3 Demo for EMP-003", use_container_width=True):
        with st.spinner("Running V3 grounded multi-agent workflow..."):
            output = grounded_agent.learner_workflow("EMP-003")
        st.text_area("Quick V3 Demo Output", output, height=650)

with tab2:
    st.markdown("## Learner Intelligence Console")

    if learners.empty:
        st.error("Learner data not found.")
    else:
        employee_id = st.selectbox(
            "Select synthetic learner",
            learners["employee_id"].tolist(),
            index=2
        )

        learner_row = learners[learners["employee_id"] == employee_id]
        st.dataframe(learner_row, use_container_width=True)

        st.markdown("### Run AI Workflows")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Run Standard Multi-Agent Workflow", use_container_width=True):
                with st.spinner("Running standard multi-agent workflow..."):
                    output = basic_agent.learner_workflow(employee_id)
                st.text_area("Standard Workflow Output", output, height=620)

        with col2:
            if st.button("Run Advanced V2 Intelligence Workflow", use_container_width=True):
                with st.spinner("Running advanced V2 workflow..."):
                    output = advanced_agent.learner_workflow(employee_id)
                st.text_area("Advanced V2 Output", output, height=720)

        with col3:
            if st.button("Run Grounded V3 Workflow", use_container_width=True):
                with st.spinner("Running grounded V3 workflow..."):
                    output = grounded_agent.learner_workflow(employee_id)
                st.text_area("Grounded V3 Output", output, height=820)

with tab3:
    st.markdown("## Manager Centre")

    st.markdown(
        """
        This section gives manager-level synthetic readiness insights.
        It is for decision support only, not automatic employee approval or rejection.
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Run V2 Manager Intelligence Agent", use_container_width=True):
            with st.spinner("Running V2 manager workflow..."):
                output = advanced_agent.manager_workflow()
            st.text_area("V2 Manager Output", output, height=650)

    with col2:
        if st.button("Run Grounded V3 Manager Agent", use_container_width=True):
            with st.spinner("Running grounded V3 manager workflow..."):
                output = grounded_agent.manager_workflow()
            st.text_area("Grounded V3 Manager Output", output, height=750)

with tab4:
    st.markdown("## Trace Telemetry")

    trace_path = REPORTS_DIR / "agent_trace_log.json"

    if st.button("Generate Fresh V3 Trace Log", use_container_width=True):
        with st.spinner("Generating trace log from V3 workflow..."):
            grounded_agent.learner_workflow("EMP-003")
        st.success("Fresh V3 trace log generated.")

    if trace_path.exists():
        st.markdown(f"Trace file: `{trace_path}`")
        try:
            trace_data = json.loads(trace_path.read_text(encoding="utf-8"))
            st.json(trace_data)
        except Exception as e:
            st.error(f"Could not read trace log: {e}")
    else:
        st.warning("No trace log found yet. Click 'Generate Fresh V3 Trace Log'.")

with tab5:
    st.markdown("## Evaluation & Safety")

    eval_path = REPORTS_DIR / "evaluation_report.txt"

    if st.button("Run Evaluation Report", use_container_width=True):
        with st.spinner("Running evaluation script..."):
            result = subprocess.run(
                [sys.executable, str(SRC_DIR / "evaluate_gridskill_iq.py")],
                capture_output=True,
                text=True,
                cwd=str(ROOT)
            )
        if result.returncode == 0:
            st.success("Evaluation completed.")
            st.code(result.stdout)
        else:
            st.error("Evaluation failed.")
            st.code(result.stderr)

    if eval_path.exists():
        st.markdown("### Latest Evaluation Report")
        st.code(eval_path.read_text(encoding="utf-8"))
    else:
        st.warning("Evaluation report not found. Click 'Run Evaluation Report'.")

    st.markdown("### Safety Controls")
    st.markdown(
        """
        - Synthetic data only
        - No real employee or customer data
        - Safety Critic Agent checks final outputs
        - Decision-support only
        - Confidence score included
        - Trace telemetry generated
        - Evidence sources shown in V3 workflow
        """
    )

with tab6:
    st.markdown("## Architecture")

    arch_path = DOCS_DIR / "architecture.md"

    if arch_path.exists():
        st.markdown(arch_path.read_text(encoding="utf-8"))
    else:
        st.warning("Architecture document not found at docs/architecture.md")

    st.markdown("### High-Level Flow")
    st.markdown(
        """
        User Request  
        ↓  
        Foundry IQ-style Knowledge Retriever  
        ↓  
        Multi-Agent Orchestrator  
        ↓  
        Specialist Agents  
        ↓  
        Safety Critic Agent  
        ↓  
        Final Grounded Response with Sources and Trace Log
        """
    )
