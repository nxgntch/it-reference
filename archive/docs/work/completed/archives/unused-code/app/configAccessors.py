"""Configuration dictionary accessor helpers (Tier 3 consolidation).

Provides type-safe, chainable helpers for accessing config dictionaries,
eliminating repetitive .get() patterns across the codebase.

Patterns consolidated:
- Model config: access model definitions, pricing, tiers
- Agent config: access agent definitions, capabilities, cost tier
- Governance config: access budget caps, team limits
- Skill config: access skill definitions, outputs, capabilities
"""

from typing import Any, Dict, List, Optional

from app.core.deduplicationHelpers import safeGet


class ConfigAccessor:
    """Type-safe config dict accessor with sensible defaults (Tier 3 consolidation).

    Eliminates repetitive .get() patterns by providing chainable methods.
    Reduces ~20 LOC per high-access file by consolidating default extraction.

    Usage:
        accessor = ConfigAccessor(configDict)
        apiKey = accessor.getString("apiKey", "default")
        budget = accessor.getFloat("budget.monthly", 0.0)
        agents = accessor.getList("agents", [])
    """

    def __init__(self, configDict: Optional[Dict[str, Any]] = None):
        """Initialize accessor with config dict.

        Args:
            configDict: Configuration dictionary to access
        """
        self.configDict = configDict or {}

    def getString(self, key: str, default: str = "") -> str:
        """Get string value from config with sensible default.

        Args:
            key: Config key (supports dot notation: "section.key")
            default: Default value if not found

        Returns:
            String value or default
        """
        value = self._getNestedValue(key)
        return str(value) if value is not None else default

    def getFloat(self, key: str, default: float = 0.0) -> float:
        """Get float value from config with sensible default.

        Args:
            key: Config key (supports dot notation)
            default: Default value if not found

        Returns:
            Float value or default
        """
        value = self._getNestedValue(key)
        try:
            return float(value) if value is not None else default
        except (ValueError, TypeError):
            return default

    def getInt(self, key: str, default: int = 0) -> int:
        """Get integer value from config with sensible default.

        Args:
            key: Config key
            default: Default value if not found

        Returns:
            Integer value or default
        """
        value = self._getNestedValue(key)
        try:
            return int(value) if value is not None else default
        except (ValueError, TypeError):
            return default

    def getBool(self, key: str, default: bool = False) -> bool:
        """Get boolean value from config with sensible default.

        Args:
            key: Config key
            default: Default value if not found

        Returns:
            Boolean value or default
        """
        value = self._getNestedValue(key)
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "yes", "1")
        return bool(value)

    def getList(self, key: str, default: Optional[List] = None) -> List:
        """Get list value from config with sensible default.

        Args:
            key: Config key
            default: Default value if not found

        Returns:
            List value or default ([] if not specified)
        """
        if default is None:
            default = []
        value = self._getNestedValue(key)
        return value if isinstance(value, list) else default

    def getDict(self, key: str, default: Optional[Dict] = None) -> Dict:
        """Get dict value from config with sensible default.

        Args:
            key: Config key
            default: Default value if not found

        Returns:
            Dict value or default ({} if not specified)
        """
        if default is None:
            default = {}
        value = self._getNestedValue(key)
        return value if isinstance(value, dict) else default

    def _getNestedValue(self, key: str) -> Any:
        """Get value from nested dict using dot notation.

        Args:
            key: Config key with optional dot notation (e.g., "section.subsection.key")

        Returns:
            Value if found, None otherwise
        """
        parts = key.split(".")
        current = self.configDict
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
        return current


def getModelConfig(model: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Get value from model config dict (Tier 3 consolidation).

    Eliminates: model.get("tier", model.get("costTier", "standard"))
    Simplifies to: getModelConfig(model, "tier", "standard")

    Args:
        model: Model configuration dict
        key: Config key
        default: Default value if not found

    Returns:
        Value or default
    """
    return safeGet(model, key, default)


def getAgentConfig(agent: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Get value from agent config dict (Tier 3 consolidation).

    Args:
        agent: Agent configuration dict
        key: Config key
        default: Default value if not found

    Returns:
        Value or default
    """
    return safeGet(agent, key, default)


def getGovernanceValue(governance: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Get value from governance config using dot notation (Tier 3 consolidation).

    Eliminates: governance.get("teams", {}).get(teamId, {}).get("budget")
    Simplifies to: getGovernanceValue(governance, f"teams.{teamId}.budget", 0)

    Args:
        governance: Governance configuration dict
        path: Dot-notation path (e.g., "teams.engineering.budget")
        default: Default value if not found

    Returns:
        Value or default
    """
    accessor = ConfigAccessor(governance)
    return accessor._getNestedValue(path) or default
