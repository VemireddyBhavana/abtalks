from typing import Dict, Any


class MemoryMetricsTracker:
    """
    Tracks operational memory telemetry:
    - Reads
    - Writes
    - Updates
    - Deletes
    - Cache Hits
    - Cache Misses
    """

    def __init__(self):
        self.reads = 0
        self.writes = 0
        self.updates = 0
        self.deletes = 0
        self.cache_hits = 0
        self.cache_misses = 0

    def record_read(self, hit_cache: bool = False) -> None:
        self.reads += 1
        if hit_cache:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

    def record_write(self) -> None:
        self.writes += 1

    def record_update(self) -> None:
        self.updates += 1

    def record_delete(self) -> None:
        self.deletes += 1

    def get_summary(self) -> Dict[str, Any]:
        total_cache_requests = self.cache_hits + self.cache_misses
        hit_ratio = round((self.cache_hits / total_cache_requests) * 100.0, 2) if total_cache_requests > 0 else 0.0
        
        return {
            "total_reads": self.reads,
            "total_writes": self.writes,
            "total_updates": self.updates,
            "total_deletes": self.deletes,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_ratio_percentage": hit_ratio,
        }


# Singleton tracker
_memory_metrics_instance = MemoryMetricsTracker()


def get_memory_metrics() -> MemoryMetricsTracker:
    return _memory_metrics_instance
