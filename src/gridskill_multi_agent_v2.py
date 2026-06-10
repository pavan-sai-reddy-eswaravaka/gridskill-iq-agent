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


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"


class GridSkillAdvancedOrchestrator:
    """
    GridSkill IQ Advanced Orchestrator V2

    Adds:
    - agent trace logging
    - structured response summary
    - confidence scoring
    - evidence/source tracking
    - saved JSON telemetry report
    """

    def __init__(self):
        self.store = DataStore()
        self.learning_agent = LearningPathCuratorAgent()
        self.study_agent = StudyPlanGeneratorAgent()
        self.engagement_agent = EngagementAgent()
        self.assessment_agent = AssessmentAgent()
        self.manager_agent = ManagerInsightsAgent()
        self.safety_agent = SafetyCriticAgent()
        self.trace = TraceLogger(REPORTS_DIR)

    def confidence_score(self, learner, certification, work_signal):
        practice_score = int(learner["practice_score_avg"])
        hours_studied = int(learner["hours_studied"])
        recommended_hours = int(certification["recommended_hours"])
        focus_hours = int(work_signal["focus_hours_per_week"])

        study_progress = hours_studied / recommended_hours

        score = 50

        if practice_score >= 75:
            score += 20
        elif practice_score >= 65:
            score += 10

        if study_progress >= 0.8:
            score += 20
        elif study_progress >= 0.5:
            score += 10

        if focus_hours >= 15:
            score += 10
        elif focus_hours < 10:
            score -= 5

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
            self.trace.log_event(
                agent_name="GridSkill Advanced Orchestrator",
                action="Learner lookup",
                input_summary=f"employee_id={employee_id}",
                output_summary="No learner found",
                confidence="Low",
                status="Failed"
            )
            self.trace.save()
            return f"No synthetic learner found for employee_id: {employee_id}"

        work_signal = self.store.get_work_signal(employee_id)
        certification = self.store.get_certification(learner["target_certification"])

        confidence_value, confidence_level = self.confidence_score(
            learner, certification, work_signal
        )

        self.trace.log_event(
            agent_name="GridSkill Advanced Orchestrator",
            action="Initial learner routing",
            input_summary=f"employee_id={employee_id}",
            output_summary=(
                f"Matched learner {learner['learner_id']} with role {learner['role']} "
                f"and target certification {learner['target_certification']}"
            ),
            sources=["learners.csv", "work_signals.csv", "certifications.json"],
            confidence=confidence_level
        )

        learning_output = self.learning_agent.run(learner, certification)
        self.trace.log_event(
            agent_name=learning_output["agent"],
            action="Map role to certification path",
            input_summary=f"role={learner['role']}, certification={certification['id']}",
            output_summary=learning_output["output"],
            sources=learning_output["sources"],
            confidence=confidence_level
        )

        study_output = self.study_agent.run(learner, certification, work_signal)
        self.trace.log_event(
            agent_name=study_output["agent"],
            action="Generate workload-aware study plan",
            input_summary=(
                f"hours_studied={learner['hours_studied']}, "
                f"meeting_hours={work_signal['meeting_hours_per_week']}, "
                f"focus_hours={work_signal['focus_hours_per_week']}"
            ),
            output_summary=study_output["output"],
            sources=study_output["sources"],
            confidence=confidence_level
        )

        engagement_output = self.engagement_agent.run(learner, work_signal)
        self.trace.log_event(
            agent_name=engagement_output["agent"],
            action="Recommend engagement strategy",
            input_summary=f"shift_pattern={work_signal['shift_pattern']}",
            output_summary=engagement_output["output"],
            sources=engagement_output["sources"],
            confidence=confidence_level
        )

        assessment_output = self.assessment_agent.run(learner, certification)
        self.trace.log_event(
            agent_name=assessment_output["agent"],
            action="Assess readiness and generate practice questions",
            input_summary=(
                f"practice_score={learner['practice_score_avg']}, "
                f"hours_studied={learner['hours_studied']}"
            ),
            output_summary=assessment_output["output"],
            sources=assessment_output["sources"],
            confidence=confidence_level
        )

        structured_summary = {
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
            "primary_skill_gap": learner["skill_gap"],
            "sources": sorted(
                set(
                    learning_output["sources"]
                    + study_output["sources"]
                    + engagement_output["sources"]
                    + assessment_output["sources"]
                )
            )
        }

        response = self.format_advanced_response(
            learner,
            employee_id,
            structured_summary,
            [learning_output, study_output, engagement_output, assessment_output]
        )

        safety_output = self.safety_agent.run(response)
        self.trace.log_event(
            agent_name=safety_output["agent"],
            action="Safety and responsible AI validation",
            input_summary="Final learner response",
            output_summary=safety_output["output"],
            sources=["Safety rules inside SafetyCriticAgent"],
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
        insight = self.manager_agent.run(self.store.learners)

        self.trace.log_event(
            agent_name=insight["agent"],
            action="Generate team-level readiness insight",
            input_summary=f"learner_count={len(self.store.learners)}",
            output_summary=insight["output"],
            sources=insight["sources"],
            confidence="High"
        )

        response = (
            "GridSkill IQ Advanced Manager Readiness Summary\n"
            "Synthetic demonstration data only. No real employee, customer, confidential, "
            "or personally identifiable data is used.\n\n"
            f"{insight['output']}\n\n"
            "Advanced system note:\n"
            "- This is a team-level readiness view.\n"
            "- It avoids unnecessary exposure of individual learner detail.\n"
            "- It is intended for decision support, not automatic certification approval.\n"
        )

        safety_output = self.safety_agent.run(response)

        self.trace.log_event(
            agent_name=safety_output["agent"],
            action="Safety and responsible AI validation",
            input_summary="Final manager response",
            output_summary=safety_output["output"],
            sources=["Safety rules inside SafetyCriticAgent"],
            confidence="High",
            status=safety_output["status"]
        )

        trace_path = self.trace.save()

        response += "\n--- Safety Critic Agent ---\n"
        response += f"Safety status: {safety_output['status']}\n"
        response += f"Safety note: {safety_output['output']}\n"
        response += f"\n\nTrace log saved to: {trace_path}"

        return response

    def format_advanced_response(self, learner, employee_id, summary, outputs):
        lines = []

        lines.append("GridSkill IQ Advanced Learner Certification Readiness Plan")
        lines.append(
            "Synthetic demonstration data only. No real employee, customer, confidential, "
            "or personally identifiable data is used."
        )
        lines.append("")

        lines.append("Structured Decision Summary")
        lines.append(json.dumps(summary, indent=2))
        lines.append("")

        for output in outputs:
            lines.append(f"--- {output['agent']} ---")
            lines.append(output["output"])
            lines.append("")

        lines.append("Advanced Engineering Notes")
        lines.append("- Planner-executor-critic style orchestration is used.")
        lines.append("- Each agent output is logged into a JSON trace file.")
        lines.append("- Confidence is estimated from practice score, study progress and focus capacity.")
        lines.append("- Sources are tracked for every agent output.")
        lines.append("- Safety validation is applied before final output.")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--learner", type=str)
    parser.add_argument("--manager", action="store_true")
    args = parser.parse_args()

    orchestrator = GridSkillAdvancedOrchestrator()

    if args.learner:
        print(orchestrator.learner_workflow(args.learner))
    elif args.manager:
        print(orchestrator.manager_workflow())
    else:
        print("GridSkill IQ Advanced Multi-Agent System V2")
        print("Try:")
        print("python src\\gridskill_multi_agent_v2.py --learner EMP-003")
        print("python src\\gridskill_multi_agent_v2.py --manager")


if __name__ == "__main__":
    main()