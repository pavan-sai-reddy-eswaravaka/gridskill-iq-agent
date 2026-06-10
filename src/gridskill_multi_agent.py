from pathlib import Path
import argparse
import csv
import json
from collections import defaultdict


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "synthetic"
KB_DIR = ROOT / "knowledge_base"


class DataStore:
    """Loads synthetic learners, work signals, certification rules and knowledge docs."""

    def __init__(self):
        self.learners = self._load_csv(DATA_DIR / "learners.csv")
        self.work_signals = self._load_csv(DATA_DIR / "work_signals.csv")
        self.certifications = self._load_json(DATA_DIR / "certifications.json")["certifications"]
        self.knowledge_docs = self._load_knowledge_docs()

    def _load_csv(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def _load_json(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_knowledge_docs(self):
        docs = {}
        for path in KB_DIR.glob("*.md"):
            docs[path.name] = path.read_text(encoding="utf-8")
        return docs

    def get_learner(self, employee_id):
        for learner in self.learners:
            if learner["employee_id"].lower() == employee_id.lower():
                return learner
        return None

    def get_work_signal(self, employee_id):
        for signal in self.work_signals:
            if signal["employee_id"].lower() == employee_id.lower():
                return signal
        return None

    def get_certification(self, cert_id):
        for cert in self.certifications:
            if cert["id"].lower() == cert_id.lower():
                return cert
        return None


class LearningPathCuratorAgent:
    """Maps learner role to certification path using synthetic knowledge."""

    def run(self, learner, certification):
        skills = ", ".join(certification["skills"])

        return {
            "agent": "Learning Path Curator Agent",
            "output": (
                f"Role: {learner['role']}\n"
                f"Recommended certification: {certification['id']} - {certification['name']}\n"
                f"Target skills: {skills}\n"
                f"Current skill gap: {learner['skill_gap']}\n"
                f"Grounding source: grid_certification_guide.md"
            ),
            "sources": ["grid_certification_guide.md", "certifications.json"]
        }


class StudyPlanGeneratorAgent:
    """Creates workload-aware study plans using certification requirements."""

    def run(self, learner, certification, work_signal):
        studied = int(learner["hours_studied"])
        recommended = int(certification["recommended_hours"])
        remaining = max(recommended - studied, 0)

        focus_hours = int(work_signal["focus_hours_per_week"])
        meeting_hours = int(work_signal["meeting_hours_per_week"])

        if meeting_hours > 20 or focus_hours < 10:
            session = "30-minute low-disruption sessions"
            weekly_hours = min(4, max(2, focus_hours // 2))
        elif focus_hours >= 15:
            session = "60 to 90-minute focused sessions"
            weekly_hours = min(6, max(4, focus_hours // 3))
        else:
            session = "45-minute balanced sessions"
            weekly_hours = 3

        weeks_needed = max(1, (remaining + weekly_hours - 1) // weekly_hours)

        return {
            "agent": "Study Plan Generator Agent",
            "output": (
                f"Recommended remaining study hours: {remaining}\n"
                f"Suggested study style: {session}\n"
                f"Suggested weekly study hours: {weekly_hours}\n"
                f"Estimated completion time: {weeks_needed} week(s)\n"
                f"Preferred learning slot: {work_signal['preferred_learning_slot']}\n"
                f"Grounding source: workload_learning_policy.md"
            ),
            "sources": ["workload_learning_policy.md", "certifications.json"]
        }


class EngagementAgent:
    """Suggests reminder strategy using synthetic work-context signals."""

    def run(self, learner, work_signal):
        meeting_hours = int(work_signal["meeting_hours_per_week"])
        focus_hours = int(work_signal["focus_hours_per_week"])

        if "Incident" in work_signal["shift_pattern"] or meeting_hours > 20:
            reminder = "Use gentle reminders twice per week outside peak operational hours."
        elif focus_hours >= 15:
            reminder = "Use structured reminders three times per week during preferred focus windows."
        else:
            reminder = "Use short weekly reminders and protect small learning blocks."

        return {
            "agent": "Engagement Agent",
            "output": (
                f"Work pattern: {work_signal['shift_pattern']}\n"
                f"Meeting load: {meeting_hours} hours/week\n"
                f"Focus capacity: {focus_hours} hours/week\n"
                f"Reminder strategy: {reminder}\n"
                f"Grounding source: workload_learning_policy.md"
            ),
            "sources": ["workload_learning_policy.md"]
        }


class AssessmentAgent:
    """Evaluates readiness and generates grounded practice questions."""

    def run(self, learner, certification):
        practice_score = int(learner["practice_score_avg"])
        hours_studied = int(learner["hours_studied"])
        recommended_hours = int(certification["recommended_hours"])
        target_score = int(certification["target_practice_score"])

        progress_pct = (hours_studied / recommended_hours) * 100

        if practice_score >= target_score and progress_pct >= 80:
            readiness = "Ready"
        elif practice_score >= 70 and progress_pct >= 65:
            readiness = "Nearly Ready"
        elif practice_score < 65 or progress_pct < 50:
            readiness = "High Risk"
        else:
            readiness = "At Risk"

        skills = certification["skills"]
        questions = [
            f"Explain how {skills[0]} supports the learner's role.",
            f"What is one risk of poor {skills[1]} understanding in an energy organisation?",
            f"How would you apply {skills[-1]} in a grid operations or reporting scenario?"
        ]

        return {
            "agent": "Assessment Agent",
            "output": (
                f"Practice score average: {practice_score}%\n"
                f"Study progress: {progress_pct:.1f}% of recommended hours\n"
                f"Readiness decision: {readiness}\n"
                f"Practice questions:\n"
                f"1. {questions[0]}\n"
                f"2. {questions[1]}\n"
                f"3. {questions[2]}\n"
                f"Grounding source: manager_readiness_policy.md"
            ),
            "readiness": readiness,
            "sources": ["manager_readiness_policy.md", "grid_certification_guide.md"]
        }


class ManagerInsightsAgent:
    """Creates team-level readiness summaries without exposing unnecessary detail."""

    def run(self, learners):
        team_counts = defaultdict(lambda: defaultdict(int))

        for learner in learners:
            team_counts[learner["team_id"]][learner["readiness_status"]] += 1

        lines = []
        for team_id, statuses in sorted(team_counts.items()):
            high_risk = statuses.get("High Risk", 0)
            at_risk = statuses.get("At Risk", 0)
            ready = statuses.get("Ready", 0)
            nearly_ready = statuses.get("Nearly Ready", 0)

            if high_risk >= 1:
                action = "Manager review recommended due to High Risk learner presence."
            elif at_risk >= 1:
                action = "Monitor weekly and protect study time."
            else:
                action = "Team appears broadly on track."

            lines.append(
                f"{team_id}: Ready={ready}, Nearly Ready={nearly_ready}, "
                f"At Risk={at_risk}, High Risk={high_risk}. Action: {action}"
            )

        return {
            "agent": "Manager Insights Agent",
            "output": "\n".join(lines) + "\nGrounding source: manager_readiness_policy.md",
            "sources": ["manager_readiness_policy.md", "learners.csv"]
        }


class SafetyCriticAgent:
    """Checks output for safety, privacy and unsupported claims."""

    def run(self, response_text):
        issues = []

        blocked_terms = ["real patient", "real customer", "diagnosis", "medical advice", "confidential"]
        for term in blocked_terms:
            if term in response_text.lower():
                issues.append(f"Potential unsafe term detected: {term}")

        if "Synthetic" not in response_text and "synthetic" not in response_text:
            issues.append("Add clearer synthetic-data disclaimer.")

        if issues:
            status = "Needs review"
            message = "; ".join(issues)
        else:
            status = "Passed"
            message = "No obvious privacy, safety or unsupported-claim issue detected."

        return {
            "agent": "Safety Critic Agent",
            "status": status,
            "output": message
        }


class GridSkillOrchestratorAgent:
    """Coordinates all specialist agents."""

    def __init__(self):
        self.store = DataStore()
        self.learning_agent = LearningPathCuratorAgent()
        self.study_agent = StudyPlanGeneratorAgent()
        self.engagement_agent = EngagementAgent()
        self.assessment_agent = AssessmentAgent()
        self.manager_agent = ManagerInsightsAgent()
        self.safety_agent = SafetyCriticAgent()

    def learner_workflow(self, employee_id):
        learner = self.store.get_learner(employee_id)
        if learner is None:
            return f"No synthetic learner found for employee_id: {employee_id}"

        work_signal = self.store.get_work_signal(employee_id)
        certification = self.store.get_certification(learner["target_certification"])

        trace = []
        trace.append(self.learning_agent.run(learner, certification))
        trace.append(self.study_agent.run(learner, certification, work_signal))
        trace.append(self.engagement_agent.run(learner, work_signal))
        trace.append(self.assessment_agent.run(learner, certification))

        response = self._format_learner_response(employee_id, learner, trace)
        safety = self.safety_agent.run(response)

        return response + "\n\n" + self._format_safety(safety)

    def manager_workflow(self):
        insight = self.manager_agent.run(self.store.learners)

        response = (
            "GridSkill IQ Manager Readiness Summary\n"
            "Synthetic demonstration data only. No real employee, customer or confidential data is used.\n\n"
            f"{insight['output']}\n\n"
            "Agent trace:\n"
            f"- {insight['agent']}\n\n"
            "Sources used:\n"
            f"- {', '.join(insight['sources'])}"
        )

        safety = self.safety_agent.run(response)
        return response + "\n\n" + self._format_safety(safety)

    def _format_learner_response(self, employee_id, learner, trace):
        sections = [
            "GridSkill IQ Learner Certification Readiness Plan",
            "Synthetic demonstration data only. No real employee, customer or confidential data is used.",
            "",
            f"Learner ID: {learner['learner_id']}",
            f"Employee ID: {employee_id}",
            f"Team: {learner['team_id']}",
            ""
        ]

        for item in trace:
            sections.append(f"--- {item['agent']} ---")
            sections.append(item["output"])
            sections.append("")

        sections.append("Agent orchestration trace:")
        for item in trace:
            sections.append(f"- {item['agent']} completed")

        sections.append("")
        sections.append("Sources used:")
        all_sources = []
        for item in trace:
            all_sources.extend(item["sources"])
        for source in sorted(set(all_sources)):
            sections.append(f"- {source}")

        return "\n".join(sections)

    def _format_safety(self, safety):
        return (
            "--- Safety Critic Agent ---\n"
            f"Safety status: {safety['status']}\n"
            f"Safety note: {safety['output']}"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--learner", type=str, help="Run learner workflow for synthetic employee ID, example EMP-003")
    parser.add_argument("--manager", action="store_true", help="Run manager insights workflow")
    args = parser.parse_args()

    orchestrator = GridSkillOrchestratorAgent()

    if args.manager:
        print(orchestrator.manager_workflow())
    elif args.learner:
        print(orchestrator.learner_workflow(args.learner))
    else:
        print("GridSkill IQ Multi-Agent System")
        print("Try:")
        print("python src\\gridskill_multi_agent.py --learner EMP-003")
        print("python src\\gridskill_multi_agent.py --manager")


if __name__ == "__main__":
    main()
