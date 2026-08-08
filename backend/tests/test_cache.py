import pytest
from app.core.cache import InMemoryCacheManager, get_cache_manager


def test_cache_manager_operations():
    """Verifies load, get, refresh, clear, and is_ready operations in InMemoryCacheManager."""
    cache = InMemoryCacheManager()
    count = {"loads": 0}

    def loader():
        count["loads"] += 1
        return {"data": "cached_val_1"}

    # First load
    val1 = cache.load("key1", loader)
    assert val1 == {"data": "cached_val_1"}
    assert count["loads"] == 1
    assert cache.is_ready("key1") is True

    # Second fetch should hit cache without calling loader again
    val2 = cache.get("key1")
    assert val2 == {"data": "cached_val_1"}
    assert count["loads"] == 1

    # Refresh cache
    def refresh_loader():
        count["loads"] += 1
        return {"data": "cached_val_2"}

    val3 = cache.refresh("key1", refresh_loader)
    assert val3 == {"data": "cached_val_2"}
    assert count["loads"] == 2

    # Clear cache
    cache.clear("key1")
    assert cache.get("key1") is None
    assert cache.is_ready("key1") is False
