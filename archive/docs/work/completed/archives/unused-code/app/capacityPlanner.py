"""Capacity planning analytics module.

Forecast resource needs and recommend provisioning.
Used by infrastructure team for capacity planning and scaling decisions.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from app.analytics.base import BaseAnalytics


@dataclass
class ResourceForecast:
    """Resource capacity forecast."""

    resource_type: str  # cpu, memory, storage, database_connections, workers
    current_usage: float
    current_capacity: float
    utilization_pct: float
    projected_usage_30d: float
    days_until_capacity: Optional[int]
    recommended_capacity: float
    headroom_pct: float  # Recommended headroom (20-30%)
    scaling_action: str  # none, monitor, scale, urgent_scale


@dataclass
class CapacityPlan:
    """Complete capacity plan."""

    forecast_period: str  # "30d", "90d", "annual"
    growth_rate_pct: float  # Month-over-month or projected
    forecasts: Dict[str, ResourceForecast]
    bottlenecks: List[str]
    recommendations: List[str]
    estimated_cost_increase: float


class CapacityPlannerSkill(BaseAnalytics):
    """Plan capacity and resource needs."""

    def __init__(self):
        """Initialize capacity planner."""
        super().__init__()
        self.headroom_target = 0.25  # 25% headroom recommended

    def forecastResource(
        self,
        resource_type: str,
        current_usage: float,
        current_capacity: float,
        growth_history: Optional[List[float]] = None,
        forecast_days: int = 30,
    ) -> ResourceForecast:
        """Forecast resource needs.

        Args:
            resource_type: Type of resource (cpu, memory, storage, etc.)
            current_usage: Current usage amount
            current_capacity: Current capacity limit
            growth_history: Optional historical usage for trend analysis
            forecast_days: Days to forecast

        Returns:
            ResourceForecast with projected needs
        """
        utilization = self.calculateUtilization(current_usage, current_capacity)

        # Calculate growth rate
        if growth_history and len(growth_history) >= 2:
            growth_rate = self.calculateGrowthRate(growth_history)
        else:
            growth_rate = 0.05  # Default 5% monthly growth

        # Project future usage
        months_ahead = forecast_days / 30
        projected_usage = current_usage * ((1 + growth_rate) ** months_ahead)

        # Calculate days until capacity
        if growth_rate > 0 and current_usage < current_capacity:
            usage_per_day = current_usage * (growth_rate / 30)
            remaining_capacity = current_capacity - current_usage
            days_until = remaining_capacity / usage_per_day if usage_per_day > 0 else None
            days_until = int(days_until) if days_until and days_until > 0 else None
        else:
            days_until = None

        # Recommend capacity with headroom
        recommended_capacity = projected_usage * (1 + self.headroom_target)

        # Determine scaling action
        if utilization > 90:
            scaling_action = "urgent_scale"
        elif utilization > 80 or (days_until and days_until < 14):
            scaling_action = "scale"
        elif utilization > 60:
            scaling_action = "monitor"
        else:
            scaling_action = "none"

        return ResourceForecast(
            resource_type=resource_type,
            current_usage=current_usage,
            current_capacity=current_capacity,
            utilization_pct=utilization,
            projected_usage_30d=projected_usage,
            days_until_capacity=days_until,
            recommended_capacity=recommended_capacity,
            headroom_pct=self.headroom_target * 100,
            scaling_action=scaling_action,
        )

    def planConcurrency(
        self,
        current_invocations: int,
        max_concurrent: int,
        growth_rate: float = 0.05,
    ) -> Dict[str, Any]:
        """Plan concurrent capacity.

        Args:
            current_invocations: Current concurrent invocations
            max_concurrent: Current max concurrent capacity
            growth_rate: Monthly growth rate

        Returns:
            Concurrency plan with recommendations
        """
        utilization = self.calculateUtilization(current_invocations, max_concurrent)

        # Project 30 days ahead
        projected_30d = current_invocations * ((1 + growth_rate) ** 1)
        projected_90d = current_invocations * ((1 + growth_rate) ** 3)

        # Recommend new capacity (with 25% headroom)
        recommended = projected_30d * 1.25

        # Determine if autoscaling needed
        needs_autoscaling = utilization > 70 or growth_rate > 0.10

        return {
            "current_invocations": current_invocations,
            "max_concurrent": max_concurrent,
            "utilization_pct": utilization,
            "projected_30d": int(projected_30d),
            "projected_90d": int(projected_90d),
            "recommended_capacity": int(recommended),
            "needs_autoscaling": needs_autoscaling,
            "headroom_target": f"{self.headroom_target * 100:.0f}%",
            "action": "implement_autoscaling" if needs_autoscaling else "monitor",
        }

    def planDatabaseResources(
        self,
        current_connections: int,
        max_connections: int,
        current_storage_gb: float,
        max_storage_gb: float,
        growth_rate: float = 0.05,
    ) -> Dict[str, Any]:
        """Plan database resource capacity.

        Args:
            current_connections: Current active connections
            max_connections: Max connection pool size
            current_storage_gb: Current storage used
            max_storage_gb: Current storage limit
            growth_rate: Monthly growth rate

        Returns:
            Database capacity plan
        """
        conn_utilization = self.calculateUtilization(current_connections, max_connections)
        storage_utilization = self.calculateUtilization(current_storage_gb, max_storage_gb)

        # Project growth
        projected_connections = current_connections * ((1 + growth_rate) ** 1)
        projected_storage = current_storage_gb * ((1 + growth_rate) ** 1)

        # Recommend capacities
        recommended_connections = int(projected_connections * 1.25)
        recommended_storage = projected_storage * 1.25

        return {
            "connections": {
                "current": current_connections,
                "max": max_connections,
                "utilization_pct": conn_utilization,
                "projected_30d": int(projected_connections),
                "recommended": recommended_connections,
                "action": "scale" if conn_utilization > 80 else "monitor",
            },
            "storage": {
                "current_gb": current_storage_gb,
                "max_gb": max_storage_gb,
                "utilization_pct": storage_utilization,
                "projected_30d_gb": projected_storage,
                "recommended_gb": recommended_storage,
                "action": "expand" if storage_utilization > 80 else "monitor",
            },
        }

    def planWorkerThreads(
        self,
        current_threads: int,
        task_queue_depth: int,
        avg_task_duration_ms: float,
        growth_rate: float = 0.05,
    ) -> Dict[str, Any]:
        """Plan worker thread capacity.

        Args:
            current_threads: Current worker threads
            task_queue_depth: Tasks waiting in queue
            avg_task_duration_ms: Average task duration
            growth_rate: Growth rate

        Returns:
            Worker thread plan
        """
        queue_utilization = task_queue_depth > current_threads * 2

        # Calculate throughput (tasks/second)
        throughput = (
            (current_threads * 1000) / avg_task_duration_ms if avg_task_duration_ms > 0 else 0
        )

        # Project future need
        projected_tasks_per_sec = throughput * (1 + growth_rate)
        threads_needed = max(
            current_threads, int((projected_tasks_per_sec * avg_task_duration_ms / 1000) * 1.25)
        )

        return {
            "current_threads": current_threads,
            "queue_depth": task_queue_depth,
            "queue_utilization": queue_utilization,
            "throughput_tasks_per_sec": throughput,
            "projected_throughput": projected_tasks_per_sec,
            "threads_needed": threads_needed,
            "growth_rate_monthly": f"{growth_rate * 100:.1f}%",
            "action": (
                "scale" if queue_utilization or threads_needed > current_threads else "monitor"
            ),
        }

    def createCapacityPlan(
        self, current_metrics: Dict[str, Any], forecast_period: str = "30d"
    ) -> CapacityPlan:
        """Create comprehensive capacity plan.

        Args:
            current_metrics: Dict with current usage metrics
            forecast_period: Forecast period ("30d", "90d", "annual")

        Returns:
            Complete CapacityPlan
        """
        forecasts = {}
        growth_rate = current_metrics.get("growth_rate", 0.05)

        # Forecast each resource
        for resource_type in ["cpu", "memory", "storage", "database_connections", "workers"]:
            if resource_type in current_metrics:
                metric = current_metrics[resource_type]
                forecast = self.forecastResource(
                    resource_type=resource_type,
                    current_usage=metric.get("current", 0),
                    current_capacity=metric.get("capacity", 100),
                    growth_history=metric.get("history"),
                )
                forecasts[resource_type] = forecast

        # Identify bottlenecks
        bottlenecks = [
            f.resource_type
            for f in forecasts.values()
            if f.scaling_action in ["urgent_scale", "scale"]
        ]

        # Generate recommendations
        recommendations = self._generateRecommendations(forecasts, growth_rate)

        # Estimate cost increase (simplified: 10% cost per 25% capacity increase)
        total_recommended = sum(f.recommended_capacity for f in forecasts.values())
        total_current = sum(f.current_capacity for f in forecasts.values())
        capacity_increase = (
            (total_recommended - total_current) / total_current if total_current > 0 else 0
        )
        cost_increase = capacity_increase * 0.10  # 10% cost per unit

        return CapacityPlan(
            forecast_period=forecast_period,
            growth_rate_pct=growth_rate * 100,
            forecasts=forecasts,
            bottlenecks=bottlenecks,
            recommendations=recommendations,
            estimated_cost_increase=cost_increase,
        )

    def _generateRecommendations(
        self, forecasts: Dict[str, ResourceForecast], growth_rate: float
    ) -> List[str]:
        """Generate capacity recommendations.

        Args:
            forecasts: Dict of resource forecasts
            growth_rate: Growth rate

        Returns:
            List of recommendations
        """
        recommendations = []

        # Identify scaling needs
        urgent = [f for f in forecasts.values() if f.scaling_action == "urgent_scale"]
        needed = [f for f in forecasts.values() if f.scaling_action == "scale"]
        monitor = [f for f in forecasts.values() if f.scaling_action == "monitor"]

        if urgent:
            names = ", ".join([f.resource_type for f in urgent])
            recommendations.append(f"🚨 URGENT: Scale {names} immediately (>90% utilization).")

        if needed:
            names = ", ".join([f.resource_type for f in needed])
            recommendations.append(f"WARNING: NEEDED: Increase {names} capacity within 2 weeks.")

        if monitor:
            names = ", ".join([f.resource_type for f in monitor])
            recommendations.append(f"📊 MONITOR: Watch {names} for approaching limits.")

        # Growth-based recommendations
        if growth_rate > 0.15:
            recommendations.append(
                f"📈 High growth rate ({growth_rate*100:.0f}%/month). Implement autoscaling."
            )
        elif growth_rate > 0.05:
            recommendations.append(
                f"Growth rate {growth_rate*100:.0f}%/month. Plan quarterly capacity reviews."
            )

        return recommendations
