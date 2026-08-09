from app.repositories.memory_repository import MemoryRepository
from app.memory.session_snapshot import SessionSnapshotManager
from app.memory.mock_provider import MockMemoryProvider


def test_memory_repository_operations():
    repo = MemoryRepository(provider=MockMemoryProvider())
    assert repo is not None


def test_snapshot_manager():
    mgr = SessionSnapshotManager()
    assert mgr is not None
