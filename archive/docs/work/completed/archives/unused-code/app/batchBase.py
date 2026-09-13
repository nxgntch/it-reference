"""Base classes and utilities for batch processing consolidation.

Phase 6: Batch consolidation foundation.
Provides shared batch container functionality and stats tracking.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.core.statsCollector import StatsCollector


class BaseBatchMetrics:
    """Shared metrics for batch operations (cost, timing, efficiency)."""

    def __init__(self):
        """Initialize batch metrics."""
        self.createdAt: datetime = datetime.utcnow()
        self.processedAt: Optional[datetime] = None
        self.totalCost: float = 0.0
        self.estimatedSavings: float = 0.0
        self.processingTimeMs: float = 0.0

    def calculateMetrics(self, taskCount: int, baseCost: float) -> None:
        """Calculate batch efficiency metrics.

        Args:
            taskCount: Number of tasks in batch
            baseCost: Total cost before savings
        """
        if self.processedAt:
            self.processingTimeMs = (self.processedAt - self.createdAt).total_seconds() * 1000

        # Estimated savings: 5% per task after first
        savingsPercent = min(0.15, (taskCount - 1) * 0.05)
        self.estimatedSavings = baseCost * savingsPercent
        self.totalCost = baseCost - self.estimatedSavings

    def getMetrics(self) -> Dict[str, Any]:
        """Get batch metrics dict.

        Returns:
            Dict with timing, cost, and efficiency metrics
        """
        return {
            "createdAt": self.createdAt.isoformat(),
            "processedAt": self.processedAt.isoformat() if self.processedAt else None,
            "totalCost": round(self.totalCost, 4),
            "estimatedSavings": round(self.estimatedSavings, 4),
            "processingTimeMs": round(self.processingTimeMs, 1),
        }


class BaseBatchContainer(ABC, StatsCollector):
    """Abstract base for batch containers with shared functionality.

    Provides common interface for batch operations:
    - Task/request management
    - Metrics tracking
    - Statistics aggregation
    - Status management
    """

    def __init__(self, batchId: str, batchType: str = "batch"):
        """Initialize batch container.

        Args:
            batchId: Unique batch identifier
            batchType: Type of batch (for tracking)
        """
        super().__init__()
        self.batchId = batchId
        self.batchType = batchType
        self.status = "pending"  # pending, processing, completed, failed
        self.metrics = BaseBatchMetrics()
        self._items: List[Any] = []
        self._results: Dict[str, Any] = {}

    @abstractmethod
    def addItem(self, item: Any) -> bool:
        """Add item to batch. Subclass must implement compatibility check.

        Args:
            item: Item to add to batch

        Returns:
            True if added, False if incompatible
        """
        pass

    @abstractmethod
    def getItemCount(self) -> int:
        """Get number of items in batch.

        Returns:
            Item count
        """
        pass

    def setProcessing(self) -> None:
        """Mark batch as processing."""
        self.status = "processing"
        self.incrementCounter("processing_started")

    def setCompleted(self) -> None:
        """Mark batch as completed."""
        self.status = "completed"
        self.metrics.processedAt = datetime.utcnow()
        self.incrementCounter("processing_completed")

    def setFailed(self, reason: str = "unknown") -> None:
        """Mark batch as failed.

        Args:
            reason: Reason for failure
        """
        self.status = "failed"
        self.metrics.processedAt = datetime.utcnow()
        self.incrementCounter("processing_failed")

    def addResult(self, itemId: str, result: Any) -> None:
        """Add result for an item.

        Args:
            itemId: Item identifier
            result: Result value
        """
        self._results[itemId] = result

    def getResults(self) -> Dict[str, Any]:
        """Get all batch results.

        Returns:
            Dict mapping item IDs to results
        """
        return self._results.copy()

    def getStatus(self) -> Dict[str, Any]:
        """Get batch status and metadata.

        Returns:
            Dict with batchId, status, itemCount, metrics
        """
        return {
            "batchId": self.batchId,
            "batchType": self.batchType,
            "status": self.status,
            "itemCount": self.getItemCount(),
            "resultCount": len(self._results),
            "metrics": self.metrics.getMetrics(),
        }


class BatchExecutionStats:
    """Track execution statistics for a batch operation."""

    def __init__(self):
        """Initialize execution stats."""
        self.processedCount = 0
        self.failedCount = 0
        self.totalLatencyMs = 0.0
        self.totalCostProcessed = 0.0
        self.retries = 0

    def recordSuccess(self, latencyMs: float, cost: float) -> None:
        """Record successful execution.

        Args:
            latencyMs: Execution latency in milliseconds
            cost: Cost for this execution
        """
        self.processedCount += 1
        self.totalLatencyMs += latencyMs
        self.totalCostProcessed += cost

    def recordFailure(self) -> None:
        """Record failed execution."""
        self.failedCount += 1

    def recordRetry(self) -> None:
        """Record retry attempt."""
        self.retries += 1

    def getStats(self) -> Dict[str, Any]:
        """Get execution statistics.

        Returns:
            Dict with execution metrics
        """
        total = self.processedCount + self.failedCount
        avgLatency = self.totalLatencyMs / self.processedCount if self.processedCount > 0 else 0

        return {
            "processed": self.processedCount,
            "failed": self.failedCount,
            "total": total,
            "successRate": (self.processedCount / total * 100) if total > 0 else 0,
            "avgLatencyMs": round(avgLatency, 1),
            "totalLatencyMs": round(self.totalLatencyMs, 1),
            "totalCost": round(self.totalCostProcessed, 4),
            "retries": self.retries,
        }
