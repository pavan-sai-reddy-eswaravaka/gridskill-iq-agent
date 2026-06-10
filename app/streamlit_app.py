import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.append(str(SRC))

from gridskill_multi_agent import GridSkillOrchestratorAgent


st.set_page_config(
    page_title="GridSkill IQ",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ GridSkill IQ")
st.subheader("Multi-Agent Reasoning System for UK Energy Workforce Certification Readiness")

st.info(
    "Synthetic demonstration data only. No real employee, customer, confidential, "
    "or personally identifiable data is used."
)

st.write(
    "GridSkill IQ is a hackathon prototype that demonstrates a multi-agent reasoning "
    "workflow for enterprise learning and certification readiness in a synthetic UK energy organisation."
)

st.write("The system uses specialised agents for learning path curation, study planning, engagement, assessment, manager insights and safety review.")

agent = GridSkillOrchestratorAgent()

tab1, tab2, tab3, tab4 = st.tabs(
    ["Learner Readiness Agent", "Manager Insights Agent", "System Architecture", "Evaluation & Safety"]
)

with tab1:
    st.header("Learner Certification Readiness Workflow")

    employee_id = st.selectbox(
        "Choose a synthetic employee",
        ["EMP-001", "EMP-002", "EMP-003", "EMP-004", "EMP-005", "EMP-006"]
    )

    if st.button("Run Learner Multi-Agent Workflow"):
        response = agent.learner_workflow(employee_id)
        st.text_area("Agent Output", response, height=650)

with tab2:
    st.header("Manager Team Readiness Summary")

    if st.button("Run Manager Insights Workflow"):
        response = agent.manager_workflow()
        st.text_area("Manager Insights Output", response, height=500)

with tab3:
    st.header("GridSkill IQ Architecture")

    st.code(
        "User Request\n"
        "   ↓\n"
        "GridSkill Orchestrator Agent\n"
        "   ↓\n"
        "Learning Path Curator Agent\n"
        "   ↓\n"
        "Study Plan Generator Agent\n"
        "   ↓\n"
        "Engagement Agent\n"
        "   ↓\n"
        "Assessment Agent\n"
        "   ↓\n"
        "Manager Insights Agent\n"
        "   ↓\n"
        "Safety Critic Agent\n"
        "   ↓\n"
        "Final Grounded Response"
    )

    st.subheader("Microsoft IQ Alignment")

    st.write("Foundry IQ concept: Synthetic knowledge base documents ground learning recommendations and assessment questions.")
    st.write("Work IQ concept: Synthetic work signals such as meeting hours, focus hours and shift patterns guide study scheduling.")
    st.write("Fabric IQ concept: Synthetic semantic model links learner, role, certification, skills, readiness score and recommended hours.")

    st.subheader("Responsible AI Controls")

    st.write("- Synthetic data only")
    st.write("- No PII")
    st.write("- No confidential information")
    st.write("- Safety critic checks final output")
    st.write("- Sources are listed in the agent response")
    st.write("- Human oversight recommended for real-world use")
with tab4:
    st.header("Evaluation & Safety Report")

    st.write(
        "GridSkill IQ includes a lightweight evaluation suite to check that the multi-agent workflow, "
        "safety disclaimer, sources, manager summary and readiness outputs are working correctly."
    )

    report_path = ROOT / "reports" / "evaluation_report.txt"

    if report_path.exists():
        report_text = report_path.read_text(encoding="utf-8")
        st.text_area("Evaluation Report", report_text, height=500)
    else:
        st.warning("Evaluation report not found. Run: python src\\evaluate_gridskill_iq.py")

    st.subheader("Responsible AI Positioning")
    st.write("- Uses synthetic demo data only")
    st.write("- Does not use real employee, customer, confidential or personal data")
    st.write("- Lists grounding sources in the agent response")
    st.write("- Includes a Safety Critic Agent")
    st.write("- Designed as decision support, not automatic certification approval")