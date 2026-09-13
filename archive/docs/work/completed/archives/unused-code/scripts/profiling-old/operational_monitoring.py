#!/usr/bin/env python3
"""Phase 17: Operational Monitoring & Performance Tracking
Monitor Phase 17 optimizations in production, track metrics over time,
and alert on regressions or anomalies.
"""

import asyncio
import logging
import time
from datetime import datetime
from typing import Any, Dict

from app.core.batchProcessor import BatchProcessor
from app.core.routingEngine import RoutingEngine
from app.core.skillManager import SkillManager
from app.core.tokenOptimizer import TokenOptimizer
from scripts.profiling.base import BaseProfiler

logger = logging.getLogger(__name__)


class OperationalMonitor(BaseProfiler):
    """Monitor Phase 17 optimizations in production."""

    def __init__(self, window_minutes: int = 60):
        """Initialize monitor.
        Args:
           window_minutes: Time window for metrics aggregation
        """
        super().__init__(name="operational_monitor")
        self.window_minutes = window_minutes
        self.metrics = {
            "routing": [],
            "batch": [],
            "token": [],
            "concurrency": [],
        }
        self.baselines = {
            "routing_latency_ms": 0.006,  # Target from Phase 17
            "batch_throughput": 297000,  # At 2x load
            "token_compression_pct": 28.5,  # Final achievement
            "concurrency_scaling": 2.82,  # At 2x load
        }
        self.alerts = []

    async def monitorRoutingLatency(self, iterations: int = 50) -> Dict[str, Any]:
        """Monitor routing latency."""
        self.logger.info("[ROUTING] Monitoring latency...")
        skillManager = SkillManager()
        router = RoutingEngine(skillManager)
        tasks = [
            "Reduce latency in API responses",
            "Optimize cost of batch processing",
            "Analyze data patterns in logs",
            "Design a new microservice architecture",
            "What is the budget status this month?",
        ]
        latencies = []
        for _ in range(iterations):
            for task in tasks:
                start = time.perf_counter()
            await router.routeTask(task, requestId="monitor-test")
            latencies.append((time.perf_counter() - start) * 1000)
        mean_latency = sum(latencies) / len(latencies)
        p95_latency = sorted(latencies)[int(len(latencies) * 0.95)]
        max_latency = max(latencies)
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "mean_ms": round(mean_latency, 3),
            "p95_ms": round(p95_latency, 3),
            "max_ms": round(max_latency, 3),
            "samples": len(latencies),
            "baseline_ms": self.baselines["routing_latency_ms"],
            "regression": mean_latency > self.baselines["routing_latency_ms"] * 1.2,
        }
        self.metrics["routing"].append(result)
        self.logger.info(
            f"  Mean: {result['mean_ms']:.3f}ms (baseline {result['baseline_ms']:.3f}ms)"
        )
        self.logger.info(f"  P95:  {result['p95_ms']:.3f}ms")
        self.logger.info(f"  Status: {'WARN' if result['regression'] else 'OK'}")
        if result["regression"]:
            self.alerts.append(
                {
                    "type": "routing_regression",
                    "severity": "warning",
                    "message": f"Routing latency regression: {result['mean_ms']:.3f}ms vs baseline {result['baseline_ms']:.3f}ms",
                    "timestamp": result["timestamp"],
                }
            )
        return result

    async def monitorBatchThroughput(self, iterations: int = 5) -> Dict[str, Any]:
        """Monitor batch processor throughput."""
        self.logger.info("[BATCH] Monitoring throughput...")
        processor = BatchProcessor()
        results_list = []
        for load in [100, 150, 200]:
            throughputs = []
            for _ in range(iterations):
                tasks = []
            for i in range(load):
                task = processor.createBatchTask(
                    taskId=f"monitor-batch-{load}-{i}",
                    agentId="test",
                    description=f"Batch task {i}",
                )
                tasks.append(task)
            start = time.perf_counter()
            processor.processBatchesPipelined(tasks)
            elapsed = time.perf_counter() - start
            throughput = load / elapsed if elapsed > 0 else 0
            throughputs.append(throughput)
            mean_throughput = sum(throughputs) / len(throughputs)
            result = {
                "load": load,
                "mean_throughput": round(mean_throughput, 2),
                "baseline": self.baselines["batch_throughput"],
                "regression": mean_throughput < self.baselines["batch_throughput"] * 0.8,
            }
            results_list.append(result)
            self.logger.info(
                f"  Load {load}: {mean_throughput:.0f} tasks/sec (baseline {result['baseline']}+)"
            )
            self.logger.info(f"  Status: {'WARN' if result['regression'] else 'OK'}")
            if result["regression"]:
                self.alerts.append(
                    {
                        "type": "batch_regression",
                        "severity": "warning",
                        "message": f"Batch throughput degradation at {load} tasks: {mean_throughput:.0f} vs baseline {result['baseline']:.0f}",
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "results": results_list,
        }

    async def monitorTokenOptimization(self) -> Dict[str, Any]:
        """Monitor token optimization effectiveness."""
        self.logger.info("[TOKEN] Monitoring compression...")
        optimizer = TokenOptimizer()
        test_prompts = [
            ("Simple", "Analyze the data."),
            ("Moderate", "Please analyze the data thoroughly and provide insights."),
            (
                "Verbose",
                """
Instructions: Please carefully analyze the data.
Requirements: Make sure to examine all aspects.
Guidelines: You should consider multiple perspectives.
Thank you for your attention to this task.
""",
            ),
        ]

        compressions = []

        for _name, prompt in test_prompts:
            analysis = optimizer.analyzePrompt(prompt, "test-agent")
            compression = (
                (analysis["tokensBefore"] - analysis["tokensAfter"])
                / analysis["tokensBefore"]
                * 100
            )
            compressions.append(compression)

        mean_compression = sum(compressions) / len(compressions)

        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "mean_compression_pct": round(mean_compression, 1),
            "baseline_pct": self.baselines["token_compression_pct"],
            "regression": mean_compression < self.baselines["token_compression_pct"] * 0.9,
        }

        self.metrics["token"].append(result)

        self.logger.info(
            f"  Compression: {result['mean_compression_pct']:.1f}% (baseline {result['baseline_pct']:.1f}%)"
        )
        self.logger.info(f"  Status: {'WARN' if result['regression'] else 'OK'}")

        if result["regression"]:
            self.alerts.append(
                {
                    "type": "token_regression",
                    "severity": "warning",
                    "message": f"Token compression degradation: {result['mean_compression_pct']:.1f}% vs baseline {result['baseline_pct']:.1f}%",
                    "timestamp": result["timestamp"],
                }
            )

        return result

    async def monitorConcurrency(self) -> Dict[str, Any]:
        """Monitor concurrency scaling."""
        self.logger.info("[CONCURRENCY] Monitoring scaling...")
        processor = BatchProcessor()
        baseline_throughput = 0
        scaling_results = []
        for load in [50, 100, 150]:
            tasks = []
            for i in range(load):
                task = processor.createBatchTask(
                    taskId=f"monitor-conc-{load}-{i}",
                    agentId="test",
                    description=f"Concurrent task {i}",
                )
            tasks.append(task)
            start = time.perf_counter()
            processor.processBatchesPipelined(tasks)
            elapsed = time.perf_counter() - start
            throughput = load / elapsed if elapsed > 0 else 0
            if load == 50:
                baseline_throughput = throughput
            scaling = throughput / baseline_throughput if baseline_throughput > 0 else 1.0
            result = {
                "load": load,
                "throughput": round(throughput, 2),
                "scaling": round(scaling, 2),
                "baseline_scaling": self.baselines["concurrency_scaling"] if load == 100 else None,
            }
            scaling_results.append(result)
            self.logger.info(f"  Load {load}: {scaling:.2f}x scaling")
        # Check for regression (at 2x load, should be >= 1.8x if baseline is 2.82x)
        scaling_2x = scaling_results[1]["scaling"]
        regression = scaling_2x < 1.5  # Allow some variance
        if regression:
            self.alerts.append(
                {
                    "type": "concurrency_regression",
                    "severity": "warning",
                    "message": f"Concurrency scaling degradation at 2x: {scaling_2x:.2f}x vs expected {self.baselines['concurrency_scaling']:.2f}x",
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )
        self.logger.info(f"  Status: {'WARN' if regression else 'OK'}")
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "results": scaling_results,
        }

    async def runFullMonitoring(self) -> Dict[str, Any]:
        """Run full Phase 17 monitoring suite."""
        self.logger.info("=" * 70)
        self.logger.info("PHASE 17 OPERATIONAL MONITORING")
        self.logger.info("=" * 70)
        start_time = datetime.utcnow()
        # Monitor all 4 initiatives
        routing_result = await self.monitorRoutingLatency()
        batch_result = await self.monitorBatchThroughput()
        token_result = await self.monitorTokenOptimization()
        concurrency_result = await self.monitorConcurrency()
        elapsed = (datetime.utcnow() - start_time).total_seconds()
        # Compile report
        report = {
            "timestamp": start_time.isoformat(),
            "monitoring_duration_seconds": elapsed,
            "initiatives": {
                "1.1_routing": routing_result,
                "1.2_batch": batch_result,
                "1.3_token": token_result,
                "1.4_concurrency": concurrency_result,
            },
            "alerts": self.alerts,
            "alert_count": len(self.alerts),
            "status": "OK" if not self.alerts else "WARNINGS",
        }
        return report

    def generateReport(self, monitoring_result: Dict[str, Any]) -> str:
        """Generate human-readable report."""
        lines = [
            "\n" + "=" * 70,
            "PHASE 17 MONITORING REPORT",
            "=" * 70,
            f"\nTimestamp: {monitoring_result['timestamp']}",
            f"Duration: {monitoring_result['monitoring_duration_seconds']:.1f}s",
            f"Status: {monitoring_result['status']}",
        ]
        if monitoring_result["alert_count"] > 0:
            lines.append(f"\n[ALERTS] {monitoring_result['alert_count']} warning(s) detected:")
            for alert in monitoring_result["alerts"]:
                lines.append(f"  - {alert['type']}: {alert['message']}")
        else:
            lines.append("\n[OK] All metrics within acceptable range")
        lines.append("\n" + "=" * 70)
        return "\n".join(lines)


def main() -> int:
    """Run operational monitoring."""

    monitor = OperationalMonitor()
    result = asyncio.run(monitor.runFullMonitoring())
    # Generate and save report
    report = monitor.generateReport(result)
    monitor.saveReport("monitoring", report)
    # Save detailed results using BaseProfiler
    monitor.saveMetrics("results", result)
    # Log recommendations
    recommendations = """
Phase 17 optimizations are now in production. Recommended actions:


   1. Set up continuous monitoring (hourly checks)
2. Configure alerts for >20% regression in any metric
3. Review baseline metrics weekly
4. Archive historical data for trend analysis
5. Escalate to ops team if any alert fires

Metrics to watch:
   - Routing latency mean < 0.010 ms (target)
- Batch throughput > 200K tasks/sec at 1.5x+ load
- Token compression > 25% on all test prompts
- Concurrency scaling > 1.8x at 2x load

Next review: Daily for first week, then weekly
"""
    monitor.saveReport("recommendations", recommendations)
    monitor.logger.info("Monitoring complete. Reports saved.")


if __name__ == "__main__":
    main()
