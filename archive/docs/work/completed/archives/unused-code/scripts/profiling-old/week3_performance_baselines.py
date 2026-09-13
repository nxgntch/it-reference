#!/usr/bin/env python3
"""Capture Phase 17 Week 3 performance baselines for routing and batch optimization."""

import asyncio
import logging
import time
from datetime import datetime
from typing import Any, Dict

from app.core.batchProcessor import BatchProcessor
from app.core.routingEngine import RoutingEngine
from app.core.skillManager import SkillManager
from scripts.profiling.base import BaseProfiler

logger = logging.getLogger(__name__)


class Week3PerformanceBaselines(BaseProfiler):
    """Capture Phase 17 Week 3 performance baselines."""

    def __init__(self):
        """Initialize performance baseline capture."""
        super().__init__(name="week3_performance_baselines")

    async def captureRoutingBaseline(self) -> Dict[str, Any]:
        """Capture routing engine performance baseline.
        Returns:
           Dict with routing performance metrics
        """
        self.logger.info("PHASE 17 WEEK 3: ROUTING ENGINE PERFORMANCE BASELINE")
        skillManager = SkillManager()
        router = RoutingEngine(skillManager)
        test_tasks = [
            "Reduce latency in API responses",
            "Optimize cost of batch processing",
            "Analyze data patterns in logs",
            "Design a new microservice architecture",
            "What is the budget status this month?",
            "Handle performance issues in the system",
        ]
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "phase": "17.3",
            "week": 3,
            "component": "routing_engine",
            "baseline_type": "performance_pre_week2_validation",
            "test_cases": len(test_tasks),
            "individual_latencies": [],
            "latency_stats": {},
        }
        self.logger.info(f"Testing routing latency with {len(test_tasks)} task types...")
        latencies = []
        for i, task in enumerate(test_tasks, 1):
            start_time = time.perf_counter()
            result = await router.routeTask(task, requestId=f"test-{i}")
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            latencies.append(elapsed_ms)
            selected_team = result.get("selected_team", "unknown")
            self.logger.info(
                f"Task {i}: {task[:40]:40s} -> {selected_team:15s} ({elapsed_ms:.3f} ms)"
            )
            results["individual_latencies"].append(
                {
                    "task_num": i,
                    "task": task[:60],
                    "selected_team": selected_team,
                    "latency_ms": round(elapsed_ms, 3),
                }
            )
        # Calculate statistics
        if latencies:
            latencies_sorted = sorted(latencies)
            results["latency_stats"] = {
                "min_ms": round(min(latencies), 3),
                "max_ms": round(max(latencies), 3),
                "mean_ms": round(sum(latencies) / len(latencies), 3),
                "median_ms": round(latencies_sorted[len(latencies_sorted) // 2], 3),
                "p95_ms": round(latencies_sorted[int(len(latencies_sorted) * 0.95)], 3),
                "p99_ms": round(latencies_sorted[int(len(latencies_sorted) * 0.99)], 3),
            }
        self.logger.info("ROUTING LATENCY STATISTICS")
        for key, value in results["latency_stats"].items():
            self.logger.info(f"{key:10s}: {value:.3f} ms")
        return results

    def captureBatchBaseline(self) -> Dict[str, Any]:
        """Capture batch processor performance baseline.
        Returns:
           Dict with batch processing performance metrics
        """
        self.logger.info("PHASE 17 WEEK 3: BATCH PROCESSOR PERFORMANCE BASELINE")
        processor = BatchProcessor()
        # Create test tasks of various complexities
        test_scenarios = [
            {"name": "light", "count": 10, "agent": "coordinator", "complexity": "low"},
            {"name": "medium", "count": 25, "agent": "researcher", "complexity": "moderate"},
            {"name": "heavy", "count": 50, "agent": "architect", "complexity": "high"},
        ]
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "phase": "17.3",
            "week": 3,
            "component": "batch_processor",
            "baseline_type": "performance_pre_week2_validation",
            "scenarios": [],
        }
        self.logger.info(f"Testing batch processing with {len(test_scenarios)} load scenarios...")
        for scenario in test_scenarios:
            self.logger.info(
                f"Scenario: {scenario['name']:10s} (batch size: {scenario['count']:3d} tasks)"
            )
            # Create tasks
            tasks = []
            for i in range(scenario["count"]):
                task = processor.createBatchTask(
                    taskId=f"{scenario['name']}-task-{i}",
                    agentId=scenario["agent"],
                    description=f"Task {i} - {scenario['complexity']} complexity work",
                )
            tasks.append(task)
            # Time the batching suggestion
            start_time = time.perf_counter()
            suggested_batches = processor.suggestBatching(tasks)
            batching_time_ms = (time.perf_counter() - start_time) * 1000
            # Time the pipeline processing
            start_time = time.perf_counter()
            processor.processBatchesPipelined(tasks)
            pipeline_time_ms = (time.perf_counter() - start_time) * 1000
            throughput = (
                scenario["count"] / (pipeline_time_ms / 1000) if pipeline_time_ms > 0 else 0
            )
            self.logger.info(f"Batching time:    {batching_time_ms:7.3f} ms")
            self.logger.info(f"Pipeline time:    {pipeline_time_ms:7.3f} ms")
            self.logger.info(f"Throughput:       {throughput:7.1f} tasks/sec")
            self.logger.info(f"Batches created:  {len(suggested_batches):3d}")
            results["scenarios"].append(
                {
                    "scenario_name": scenario["name"],
                    "task_count": scenario["count"],
                    "agent": scenario["agent"],
                    "complexity": scenario["complexity"],
                    "batches_created": len(suggested_batches),
                    "batching_time_ms": round(batching_time_ms, 3),
                    "pipeline_time_ms": round(pipeline_time_ms, 3),
                    "throughput_tasks_per_sec": round(throughput, 2),
                }
            )
        # Calculate aggregate throughput
        total_tasks = sum(s["task_count"] for s in results["scenarios"])
        total_time_ms = sum(s["pipeline_time_ms"] for s in results["scenarios"])
        aggregate_throughput = total_tasks / (total_time_ms / 1000) if total_time_ms > 0 else 0
        results["aggregate"] = {
            "total_tasks_processed": total_tasks,
            "total_time_ms": round(total_time_ms, 3),
            "aggregate_throughput_tasks_per_sec": round(aggregate_throughput, 2),
        }
        self.logger.info("BATCH PROCESSOR SUMMARY")
        self.logger.info(f"Total tasks processed: {results['aggregate']['total_tasks_processed']}")
        self.logger.info(f"Total time: {results['aggregate']['total_time_ms']:.3f} ms")
        self.logger.info(
            f"Aggregate throughput: {results['aggregate']['aggregate_throughput_tasks_per_sec']:.2f} tasks/sec"
        )
        return results

    def saveResults(self, routing_results: Dict[str, Any], batch_results: Dict[str, Any]) -> None:
        """Save performance baselines to file.
        Args:
           routing_results: Routing engine performance results
           batch_results: Batch processor performance results
        """
        combined = {
            "timestamp": datetime.utcnow().isoformat(),
            "phase": "17.3",
            "week": 3,
            "baseline_type": "performance_pre_optimization",
            "routing": routing_results,
            "batch": batch_results,
        }
        self.saveMetrics(combined, "phase17_week3_performance_baselines")

    async def run(self):
        """Run performance baseline capture."""
        self.logger.info("Phase 17 Week 3: Capture Performance Baselines")
        self.logger.info("Starting: Monday, September 8, 2026 - Performance Validation")
        # Capture routing baseline
        routing_results = await self.captureRoutingBaseline()
        # Capture batch baseline
        batch_results = self.captureBatchBaseline()
        # Save results
        self.saveResults(routing_results, batch_results)
        self.logger.info("NEXT STEPS")
        self.logger.info(
            "1. Review performance baselines in phase17_week3_performance_baselines.json"
        )
        self.logger.info("2. Compare to expected improvements from Week 2 optimizations")
        self.logger.info("3. Wed 9/10: Begin concurrency baseline capture")
        self.logger.info("4. Thu 9/11: Implement first-round token optimizations")
        self.logger.info("5. Fri 9/12: Validate all improvements achieved")
        self.logger.info("Week 3 Targets:")
        self.logger.info("  - Routing: Verify >= 20% latency reduction")
        self.logger.info("  - Batch: Verify >= 25% throughput increase")
        self.logger.info("  - Token: Achieve ≥10% reduction (target 15% by Week 4)")
        self.logger.info("  - Concurrency: Identify bottlenecks for Week 4 optimization")


if __name__ == "__main__":
    baseline = Week3PerformanceBaselines()
    asyncio.run(baseline.run())
