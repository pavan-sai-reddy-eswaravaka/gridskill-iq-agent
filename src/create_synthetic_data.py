from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]

data_dir = ROOT / "data" / "synthetic"
kb_dir = ROOT / "knowledge_base"

data_dir.mkdir(parents=True, exist_ok=True)
kb_dir.mkdir(parents=True, exist_ok=True)

learners = [
    {
        "learner_id": "L-1001",
        "employee_id": "EMP-001",
        "team_id": "TEAM-A",
        "role": "Grid Operations Analyst",
        "target_certification": "PL-300",
        "practice_score_avg": 68,
        "hours_studied": 14,
        "skill_gap": "Power BI modelling",
        "readiness_status": "At Risk"
    },
    {
        "learner_id": "L-1002",
        "employee_id": "EMP-002",
        "team_id": "TEAM-A",
        "role": "Smart Meter Data Analyst",
        "target_certification": "DP-900",
        "practice_score_avg": 78,
        "hours_studied": 21,
        "skill_gap": "Data fundamentals",
        "readiness_status": "Nearly Ready"
    },
    {
        "learner_id": "L-1003",
        "employee_id": "EMP-003",
        "team_id": "TEAM-B",
        "role": "Cybersecurity Support Analyst",
        "target_certification": "SC-900",
        "practice_score_avg": 62,
        "hours_studied": 11,
        "skill_gap": "Identity and access concepts",
        "readiness_status": "High Risk"
    },
    {
        "learner_id": "L-1004",
        "employee_id": "EMP-004",
        "team_id": "TEAM-B",
        "role": "Renewable Energy Operations Trainee",
        "target_certification": "AI-900",
        "practice_score_avg": 74,
        "hours_studied": 19,
        "skill_gap": "AI use cases and responsible AI",
        "readiness_status": "Nearly Ready"
    },
    {
        "learner_id": "L-1005",
        "employee_id": "EMP-005",
        "team_id": "TEAM-C",
        "role": "Power BI Reporting Analyst",
        "target_certification": "PL-300",
        "practice_score_avg": 84,
        "hours_studied": 27,
        "skill_gap": "DAX optimisation",
        "readiness_status": "Ready"
    },
    {
        "learner_id": "L-1006",
        "employee_id": "EMP-006",
        "team_id": "TEAM-C",
        "role": "Energy Forecasting Analyst",
        "target_certification": "DP-900",
        "practice_score_avg": 58,
        "hours_studied": 9,
        "skill_gap": "Relational and analytical data concepts",
        "readiness_status": "High Risk"
    }
]

work_signals = [
    {
        "employee_id": "EMP-001",
        "meeting_hours_per_week": 21,
        "focus_hours_per_week": 9,
        "preferred_learning_slot": "Morning",
        "shift_pattern": "Early operations rota"
    },
    {
        "employee_id": "EMP-002",
        "meeting_hours_per_week": 14,
        "focus_hours_per_week": 17,
        "preferred_learning_slot": "Afternoon",
        "shift_pattern": "Standard day rota"
    },
    {
        "employee_id": "EMP-003",
        "meeting_hours_per_week": 24,
        "focus_hours_per_week": 7,
        "preferred_learning_slot": "Evening",
        "shift_pattern": "Incident support rota"
    },
    {
        "employee_id": "EMP-004",
        "meeting_hours_per_week": 16,
        "focus_hours_per_week": 15,
        "preferred_learning_slot": "Morning",
        "shift_pattern": "Hybrid operations rota"
    },
    {
        "employee_id": "EMP-005",
        "meeting_hours_per_week": 12,
        "focus_hours_per_week": 20,
        "preferred_learning_slot": "Afternoon",
        "shift_pattern": "Reporting team rota"
    },
    {
        "employee_id": "EMP-006",
        "meeting_hours_per_week": 23,
        "focus_hours_per_week": 8,
        "preferred_learning_slot": "Morning",
        "shift_pattern": "Forecasting support rota"
    }
]

certifications = {
    "certifications": [
        {
            "id": "PL-300",
            "name": "Power BI Data Analyst",
            "recommended_hours": 28,
            "target_practice_score": 75,
            "skills": ["Power BI modelling", "DAX", "visual analytics", "data quality reporting"]
        },
        {
            "id": "DP-900",
            "name": "Azure Data Fundamentals",
            "recommended_hours": 22,
            "target_practice_score": 75,
            "skills": ["relational data", "analytical workloads", "data governance", "cloud data basics"]
        },
        {
            "id": "AI-900",
            "name": "Azure AI Fundamentals",
            "recommended_hours": 18,
            "target_practice_score": 75,
            "skills": ["AI workloads", "responsible AI", "machine learning basics", "computer vision basics"]
        },
        {
            "id": "SC-900",
            "name": "Security, Compliance, and Identity Fundamentals",
            "recommended_hours": 24,
            "target_practice_score": 75,
            "skills": ["identity", "access control", "security posture", "compliance concepts"]
        }
    ]
}

def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

write_csv(data_dir / "learners.csv", learners)
write_csv(data_dir / "work_signals.csv", work_signals)

with open(data_dir / "certifications.json", "w", encoding="utf-8") as f:
    json.dump(certifications, f, indent=2)

(kb_dir / "grid_certification_guide.md").write_text(
"""# GridSkill IQ Certification Guide Synthetic

This document is synthetic and created only for hackathon demonstration.

Grid Operations Analyst:
- Recommended certification: PL-300
- Key skills: Power BI modelling, operational dashboards, DAX, data quality checks
- Recommended study pattern: 1 hour daily plus one weekly practice assessment

Smart Meter Data Analyst:
- Recommended certification: DP-900
- Key skills: data fundamentals, analytical workloads, data quality, cloud data basics
- Recommended study pattern: 1 hour daily for 3 weeks

Cybersecurity Support Analyst:
- Recommended certification: SC-900
- Key skills: identity, access control, security posture, compliance concepts
- Recommended study pattern: 1 hour daily plus scenario-based revision

Renewable Energy Operations Trainee:
- Recommended certification: AI-900
- Key skills: AI workloads, responsible AI, forecasting use cases, automation basics
- Recommended study pattern: 45 minutes daily plus weekly checkpoint

Readiness rule:
- A learner is Ready when practice score is 75 or above and studied hours meet at least 80 percent of recommended hours.
""",
encoding="utf-8"
)

(kb_dir / "workload_learning_policy.md").write_text(
"""# Workload and Learning Policy Synthetic

This document is synthetic and created only for hackathon demonstration.

Learning should be scheduled around workload capacity.

Guidelines:
- If meeting hours are above 20 per week, avoid long study sessions.
- If focus hours are below 10 per week, recommend shorter study blocks.
- If focus hours are 15 or more per week, recommend 60 to 90 minute study blocks.
- Preferred learning slot should be respected where possible.
- Learners on incident support rota should receive low-disruption reminders.

Manager guidance:
- Teams with multiple High Risk learners should receive manager-level attention.
- Readiness risk should be reviewed weekly.
- The system should not expose unnecessary personal information.
""",
encoding="utf-8"
)

(kb_dir / "manager_readiness_policy.md").write_text(
"""# Manager Readiness Policy Synthetic

This document is synthetic and created only for hackathon demonstration.

Manager insights should summarise readiness at team level.

Risk rules:
- High Risk: practice score below 65 or studied hours below 50 percent of recommended hours.
- At Risk: practice score between 65 and 74 or insufficient study hours.
- Nearly Ready: practice score near target and study progress mostly complete.
- Ready: practice score is 75 or above and study progress is sufficient.

Recommended manager actions:
- Prioritise High Risk learners for extra support.
- Protect focus time for learners with high meeting load.
- Use team-level summaries instead of exposing sensitive individual details.
- Review certification readiness before scheduling exams.
""",
encoding="utf-8"
)

print("Synthetic data and knowledge base files created successfully.")
print(f"Created files in: {data_dir}")
print(f"Created documents in: {kb_dir}")
