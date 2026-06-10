from pathlib import Path
from datetime import datetime
import json
import uuid


class TraceLogger:
    """
    Trace logger for GridSkill IQ.

    Records each agent step, input summary, output summary, sources,
    confidence and safety status for observability.
    """

    def __init__(self, reports_dir):
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.run_id = str(uuid.uuid4())
        self.started_at = datetime.now().isoformat(timespec="seconds")
        self.events = []

    def log_event(
        self,
        agent_name,
        action,
        input_summary,
        output_summary,
        sources=None,
        confidence="Medium",
        status="Completed"
    ):
        event = {
            "run_id": self.run_id,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "agent_name": agent_name,
            "action": action,
            "input_summary": input_summary,
            "output_summary": output_summary,
            "sources": sources or [],
            "confidence": confidence,
            "status": status
        }

        self.events.append(event)

    def save(self):
        trace = {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": datetime.now().isoformat(timespec="seconds"),
            "event_count": len(self.events),
            "events": self.events
        }

        output_path = self.reports_dir / "agent_trace_log.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(trace, f, indent=2)

        return output_path
