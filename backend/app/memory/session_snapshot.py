from typing import Dict, Any, List
from app.memory.memory_models import InterviewMemory
from app.utils.helpers import get_utc_now
from app.core.logging_config import logger


class SessionSnapshotManager:
    """
    Automatically creates state snapshots at important milestones:
    - Interview started
    - Question answered
    - Evaluation completed
    - Interview finished
    Essential for session recovery and debugging.
    """

    def __init__(self):
        self._snapshots: Dict[str, List[Dict[str, Any]]] = {}

    def create_snapshot(self, session_id: str, milestone: str, memory: InterviewMemory) -> Dict[str, Any]:
        snapshot = {
            "snapshot_id": f"snap_{session_id}_{len(self._snapshots.get(session_id, [])) + 1}",
            "session_id": session_id,
            "milestone": milestone,
            "timestamp": get_utc_now(),
            "turn_count": len(memory.turns),
            "state_dump": memory.model_dump(),
        }

        if session_id not in self._snapshots:
            self._snapshots[session_id] = []
        self._snapshots[session_id].append(snapshot)

        logger.info(f"Snapshot created: Milestone '{milestone}' for session '{session_id}'.")
        return snapshot

    def get_snapshots(self, session_id: str) -> List[Dict[str, Any]]:
        return self._snapshots.get(session_id, [])
