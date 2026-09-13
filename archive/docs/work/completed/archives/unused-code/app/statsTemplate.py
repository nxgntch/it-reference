"""Shared utilities for stats initialization and management.

Consolidates dict-based stats initialization patterns to eliminate duplication
of stats structure definitions across modules.
"""

from typing import Any, ClassVar, Dict, TypeVar

T = TypeVar("T")


class StatsTemplate:
    """Base class for dict-based stats management with schema definition.

    Eliminates duplication of stats initialization and reset logic by defining
    the stats schema once and reusing it across init and reset.

    Example:
        class QueryProfiler(StatsTemplate):
            STATS_SCHEMA = {
                "total_queries": 0,
                "total_time_ms": 0.0,
                "slow_queries": 0,
            }

            def __init__(self):
                self.stats = self.initializeStats()

            def reset(self):
                self.stats = self.initializeStats()
    """

    # Override this in subclasses
    STATS_SCHEMA: ClassVar[Dict[str, Any]] = {}

    @classmethod
    def initializeStats(cls) -> Dict[str, Any]:
        """Initialize stats dict from schema (deep copy).

        Returns:
            New stats dict with schema defaults
        """
        return _deepCopyTemplate(cls.STATS_SCHEMA)

    @classmethod
    def getStatsSchema(cls) -> Dict[str, Any]:
        """Get stats schema definition.

        Returns:
            Schema dict (reference, not a copy)
        """
        return cls.STATS_SCHEMA

    def resetStats(self) -> None:
        """Reset stats dict to schema defaults."""
        self.stats = self.initializeStats()


def _deepCopyTemplate(template: Dict[str, Any]) -> Dict[str, Any]:
    """Deep copy a stats template dict.

    Recursively copies all nested dicts and lists to ensure each copy
    is independent.

    Args:
        template: Template dict to copy

    Returns:
        Deep copy of template
    """
    result = {}
    for key, value in template.items():
        if isinstance(value, dict):
            result[key] = _deepCopyTemplate(value)
        elif isinstance(value, list):
            result[key] = value.copy()
        else:
            result[key] = value
    return result


def mergeStats(baseStats: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """Merge stats updates into base stats dict.

    Recursively merges nested dicts, accumulates numeric values.

    Args:
        baseStats: Base stats dict
        updates: Updates to merge in

    Returns:
        Merged stats dict
    """
    result = _deepCopyTemplate(baseStats)

    for key, value in updates.items():
        if key not in result:
            result[key] = value
        elif isinstance(value, dict) and isinstance(result[key], dict):
            result[key] = mergeStats(result[key], value)
        elif isinstance(value, (int, float)) and isinstance(result[key], (int, float)):
            result[key] += value
        else:
            result[key] = value

    return result


def defineStatsSchema(**kwargs: Any) -> Dict[str, Any]:
    """Helper to define a stats schema as keyword arguments.

    Useful for concise, readable schema definitions.

    Example:
        STATS_SCHEMA = defineStatsSchema(
            total_queries=0,
            total_time_ms=0.0,
            slow_queries=0,
        )

    Args:
        **kwargs: Schema fields and their default values

    Returns:
        Stats schema dict
    """
    return dict(kwargs)
