from pathlib import Path
from datetime import datetime
from gridskill_multi_agent import GridSkillOrchestratorAgent


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


def check_contains(text, expected, test_name):
    if expected.lower() in text.lower():
        return {"test": test_name, "status": "PASS", "detail": f"Found: {expected}"}
    return {"test": test_name, "status": "FAIL", "detail": f"Missing: {expected}"}


def run_evaluations():
    agent = GridSkillOrchestratorAgent()
    results = []

    learner_response = agent.learner_workflow("EMP-003")
    manager_response = agent.manager_workflow()

    checks = [
        (learner_response, "Learning Path Curator Agent", "Learner workflow includes learning path agent"),
        (learner_response, "Study Plan Generator Agent", "Learner workflow includes study plan agent"),
        (learner_response, "Engagement Agent", "Learner workflow includes engagement agent"),
        (learner_response, "Assessment Agent", "Learner workflow includes assessment agent"),
        (learner_response, "Safety Critic Agent", "Learner workflow includes safety critic"),
        (learner_response, "Synthetic demonstration data only", "Learner workflow includes synthetic data disclaimer"),
        (learner_response, "SC-900", "Learner workflow maps EMP-003 to SC-900"),
        (learner_response, "High Risk", "Learner workflow identifies high-risk learner"),
        (learner_response, "Sources used", "Learner workflow includes sources"),
        (manager_response, "Manager Readiness Summary", "Manager workflow creates manager summary"),
        (manager_response, "TEAM-A", "Manager workflow includes TEAM-A"),
        (manager_response, "TEAM-B", "Manager workflow includes TEAM-B"),
        (manager_response, "TEAM-C", "Manager workflow includes TEAM-C"),
        (manager_response, "Safety status: Passed", "Manager workflow passes safety check"),
    ]

    for text, expected, test_name in checks:
        results.append(check_contains(text, expected, test_name))

    pass_count = sum(1 for r in results if r["status"] == "PASS")
    fail_count = sum(1 for r in results if r["status"] == "FAIL")

    report_lines = []
    report_lines.append("GridSkill IQ Evaluation Report")
    report_lines.append("=" * 50)
    report_lines.append(f"Generated at: {datetime.now().isoformat(timespec='seconds')}")
    report_lines.append(f"Total tests: {len(results)}")
    report_lines.append(f"Passed: {pass_count}")
    report_lines.append(f"Failed: {fail_count}")
    report_lines.append("")

    for result in results:
        report_lines.append(f"[{result['status']}] {result['test']} - {result['detail']}")

    report_text = "\n".join(report_lines)

    report_path = REPORTS_DIR / "evaluation_report.txt"
    report_path.write_text(report_text, encoding="utf-8")

    print(report_text)
    print()
    print(f"Evaluation report saved to: {report_path}")


if __name__ == "__main__":
    run_evaluations()
