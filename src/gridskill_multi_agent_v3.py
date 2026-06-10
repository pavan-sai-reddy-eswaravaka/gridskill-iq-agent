from pathlib import Path
import argparse
import json

from gridskill_multi_agent import (
    DataStore,
    LearningPathCuratorAgent,
    StudyPlanGeneratorAgent,
    EngagementAgent,
    AssessmentAgent,
    ManagerInsightsAgent,
    SafetyCriticAgent,
)

from trace_logger import TraceLogger
from knowledge_retriever import KnowledgeRetriever


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"


class GridSkillGroundedOrchestrator:
    """
    GridSkill IQ V3 - Grounded Multi-Agent Orchestrator

    Adds:
    - Foundry IQ-style synthetic knowledge retrieval
    - evidence snippets before agent decisions
    - grounded response sections
    - source/citation tracking
    - trace logging for retrieval and agent steps
    """

    def __init__(self):
        self.store = DataStore()
        self.retriever = KnowledgeRetriever()
        self.learning_agent = LearningPathCuratorAgent()
        self.study_agent = StudyPlanGeneratorAgent()
        self.engagement_agent = EngagementAgent()
        self.assessment_agent = AssessmentAgent()
        self.manager_agent = ManagerInsightsAgent()
        self.safety_agent = SafetyCriticAgent()
        self.trace = TraceLogger(REPORTS_DIR)

    def confidence_score(self, learner, certification, work_signal, evidence_count):
        practice_score = int(learner["practice_score_avg"])
        hours_studied = int(learner["hours_studied"])
        recommended_hours = int(certification["recommended_hours"])
        focus_hours = int(work_signal["focus_hours_per_week"])

        progress = hours_studied / recommended_hours

        score = 45

        if practice_score >= 75:
            score += 20
        elif practice_score >= 65:
            score += 10

        if progress >= 0.8:
            score += 20
        elif progress >= 0.5:
            score += 10

        if focus_hours >= 15:
            score += 10
        elif focus_hours < 10:
            score -= 5

        if evidence_count >= 3:
            score += 10
        elif evidence_count == 0:
            score -= 10

        score = max(0, min(score, 100))

        if score >= 80:
            level = "High"
        elif score >= 60:
            level = "Medium"
        else:
            level = "Low"

        return score, level

    def learner_workflow(self, employee_id):
        learner = self.store.get_learner(employee_id)

        if learner is None:
            return f"No synthetic learner found for employee_id: {employee_id}"

        work_signal = self.store.get_work_signal(employee_id)
        certification = self.store.get_certification(learner["target_certification"])

        evidence = self.retriever.retrieve_for_role(
            learner["role"],
            learner["target_certification"],
            learner["skill_gap"]
        )

        evidence_text = self.retriever.format_evidence(evidence)
        evidence_sources = sorted(set(item["source"] for item in evidence))

        confidence_value, confidence_level = self.confidence_score(
            learner,
            certification,
            work_signal,
            len(evidence)
        )

        self.trace.log_event(
            agent_name="Foundry IQ-style Knowledge Retriever",
            action="Retrieve grounded evidence from synthetic knowledge base",
            input_summary=(
                f"role={learner['role']}, certification={learner['target_certification']}, "
                f"skill_gap={learner['skill_gap']}"
            ),
            output_summary=f"Retrieved {len(evidence)} evidence snippets",
            sources=evidence_sources,
            confidence=confidence_level
        )

        learning_output = self.learning_agent.run(learner, certification)
        study_output = self.study_agent.run(learner, certification, work_signal)
        engagement_output = self.engagement_agent.run(learner, work_signal)
        assessment_output = self.assessment_agent.run(learner, certification)

        agent_outputs = [
            learning_output,
            study_output,
            engagement_output,
            assessment_output
        ]

        for output in agent_outputs:
            self.trace.log_event(
                agent_name=output["agent"],
                action="Execute specialist agent task",
                input_summary=f"employee_id={employee_id}",
                output_summary=output["output"],
                sources=output["sources"],
                confidence=confidence_level
            )

        structured_summary = {
            "system_version": "GridSkill IQ V3 Grounded Agent",
            "learner_id": learner["learner_id"],
            "employee_id": employee_id,
            "team_id": learner["team_id"],
            "role": learner["role"],
            "target_certification": learner["target_certification"],
            "practice_score_avg": int(learner["practice_score_avg"]),
            "hours_studied": int(learner["hours_studied"]),
            "readiness_decision": assessment_output["readiness"],
            "confidence_score": confidence_value,
            "confidence_level": confidence_level,
            "evidence_items_retrieved": len(evidence),
            "evidence_sources": evidence_sources,
            "primary_skill_gap": learner["skill_gap"]
        }

        response = self.format_response(
            learner=learner,
            employee_id=employee_id,
            summary=structured_summary,
            evidence_text=evidence_text,
            agent_outputs=agent_outputs
        )

        safety_output = self.safety_agent.run(response)

        self.trace.log_event(
            agent_name=safety_output["agent"],
            action="Safety validation",
            input_summary="Final grounded response",
            output_summary=safety_output["output"],
            sources=["SafetyCriticAgent rules"],
            confidence="High",
            status=safety_output["status"]
        )

        trace_path = self.trace.save()

        response += "\n\n--- Safety Critic Agent ---\n"
        response += f"Safety status: {safety_output['status']}\n"
        response += f"Safety note: {safety_output['output']}\n"
        response += f"\n\nTrace log saved to: {trace_path}"

        return response

    def manager_workflow(self):
        evidence = self.retriever.search(
            "manager readiness high risk learner team study hours focus hours certification",
            top_k=5
        )

        evidence_text = self.retriever.format_evidence(evidence)
        evidence_sources = sorted(set(item["source"] for item in evidence))

        self.trace.log_event(
            agent_name="Foundry IQ-style Knowledge Retriever",
            action="Retrieve manager-readiness evidence",
            input_summary="manager readiness, team risk, study support",
            output_summary=f"Retrieved {len(evidence)} evidence snippets",
            sources=evidence_sources,
            confidence="High"
        )

        insight = self.manager_agent.run(self.store.learners)

        self.trace.log_event(
            agent_name=insight["agent"],
            action="Generate manager readiness summary",
            input_summary=f"learner_count={len(self.store.learners)}",
            output_summary=insight["output"],
            sources=insight["sources"],
            confidence="High"
        )

        response = (
            "GridSkill IQ V3 Grounded Manager Readiness Summary\n"
            "Synthetic demonstration data only. No real employee, customer, confidential, "
            "or personally identifiable data is used.\n\n"
            "Grounded Evidence Retrieved:\n"
            f"{evidence_text}\n\n"
            "--- Manager Insights Agent ---\n"
            f"{insight['output']}\n\n"
            "Decision-support note:\n"
            "- This is a team-level synthetic readiness view.\n"
            "- It is intended for planning support, not automatic certification approval.\n"
            "- Manager actions should be reviewed by a human decision-maker.\n"
        )

        safety_output = self.safety_agent.run(response)

        self.trace.log_event(
            agent_name=safety_output["agent"],
            action="Safety validation",
            input_summary="Final manager response",
            output_summary=safety_output["output"],
            sources=["SafetyCriticAgent rules"],
            confidence="High",
            status=safety_output["status"]
        )

        trace_path = self.trace.save()

        response += "\n--- Safety Critic Agent ---\n"
        response += f"Safety status: {safety_output['status']}\n"
        response += f"Safety note: {safety_output['output']}\n"
        response += f"\n\nTrace log saved to: {trace_path}"

        return response

    def format_response(self, learner, employee_id, summary, evidence_text, agent_outputs):
        lines = []

        lines.append("GridSkill IQ V3 Grounded Learner Certification Readiness Plan")
        lines.append(
            "Synthetic demonstration data only. No real employee, customer, confidential, "
            "or personally identifiable data is used."
        )
        lines.append("")

        lines.append("Structured Decision Summary")
        lines.append(json.dumps(summary, indent=2))
        lines.append("")

        lines.append("Grounded Evidence Retrieved")
        lines.append(evidence_text)
        lines.append("")

        for output in agent_outputs:
            lines.append(f"--- {output['agent']} ---")
            lines.append(output["output"])
            lines.append("")

        lines.append("V3 Advanced Engineering Notes")
        lines.append("- Uses a Foundry IQ-style retrieval layer over synthetic knowledge documents.")
        lines.append("- Specialist agents operate after relevant evidence is retrieved.")
        lines.append("- Outputs include evidence sources, confidence score and safety validation.")
        lines.append("- JSON trace telemetry is saved for observability.")
        lines.append("- This is a local prototype designed to be extendable to Microsoft Foundry.")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--learner", type=str)
    parser.add_argument("--manager", action="store_true")
    args = parser.parse_args()

    orchestrator = GridSkillGroundedOrchestrator()

    if args.learner:
        print(orchestrator.learner_workflow(args.learner))
    elif args.manager:
        print(orchestrator.manager_workflow())
    else:
        print("GridSkill IQ V3 Grounded Multi-Agent System")
        print("Try:")
        print("python src\\gridskill_multi_agent_v3.py --learner EMP-003")
        print("python src\\gridskill_multi_agent_v3.py --manager")


if __name__ == "__main__":
    main()