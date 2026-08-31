#!/usr/bin/env python3
"""Phase 17 Gate Closure Validation: Final comprehensive test of all 4 initiatives."""

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


class GateClosureValidator(BaseProfiler):
    """Validate Phase 17 gate closure across all initiatives."""

    def __init__(self):
        super().__init__(name="gate_closure_validation")

    async def validateAllInitiatives(self) -> Dict[str, Any]:
        """Run final comprehensive validation of all 4 initiatives."""
        self.logger.info("=" * 80)
        self.logger.info("PHASE 17: GATE CLOSURE VALIDATION")
        self.logger.info("=" * 80)
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "phase": "17",
            "week": "5_gate_closure",
            "validation_type": "final_comprehensive",
            "initiatives": {},
            "gate_closure_criteria": {},
            "overall_status": "PENDING",
        }
        # Initiative 1.1: Routing Latency
        self.logger.info("-" * 80)
        self.logger.info("INITIATIVE 1.1: ROUTING LATENCY")
        self.logger.info("-" * 80)
        skillManager = SkillManager()
        router = RoutingEngine(skillManager)
        tasks = [
            "Reduce latency in API responses",
            "Optimize cost of batch processing",
            "Analyze data patterns in logs",
            "Design a new microservice architecture",
            "What is the budget status this month?",
            "Handle performance issues in the system",
        ]
        latencies = []
        for task in tasks:
            start = time.perf_counter()
            await router.routeTask(task, requestId="gate-test")
            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies.append(elapsed_ms)
        latencies_sorted = sorted(latencies)
        routing_result = {
            "mean_ms": round(sum(latencies) / len(latencies), 3),
            "min_ms": round(min(latencies), 3),
            "max_ms": round(max(latencies), 3),
            "p95_ms": round(latencies_sorted[int(len(latencies) * 0.95)], 3),
        }
        routing_result["pass"] = routing_result["mean_ms"] < 0.010
        results["initiatives"]["routing"] = routing_result
        self.logger.info(f"Mean latency: {routing_result['mean_ms']:.3f} ms")
        self.logger.info(
            f"Target: <0.010 ms | Status: {'PASS' if routing_result['pass'] else 'FAIL'}"
        )
        # Initiative 1.2: Batch Throughput
        self.logger.info("-" * 80)
        self.logger.info("INITIATIVE 1.2: BATCH PROCESSOR THROUGHPUT")
        self.logger.info("-" * 80)
        processor = BatchProcessor()
        batch_results = []
        for load_level in [50, 100, 150]:
            tasks = []
            for i in range(load_level):
                task = processor.createBatchTask(
                    taskId=f"gate-batch-{load_level}-{i}",
                    agentId="test",
                    description=f"Batch task {i}",
                )
            tasks.append(task)
            start = time.perf_counter()
            processor.processBatchesPipelined(tasks)
            elapsed = time.perf_counter() - start
            throughput = load_level / elapsed if elapsed > 0 else 0
            batch_results.append(
                {
                    "load": load_level,
                    "throughput": round(throughput, 2),
                    "pass": throughput >= 50000,
                }
            )
            self.logger.info(
                f"Load {load_level:3d}: {throughput:10.1f} tasks/sec - {'PASS' if throughput >= 50000 else 'FAIL'}"
            )
        results["initiatives"]["batch"] = {
            "results": batch_results,
            "aggregate_pass": all(r["pass"] for r in batch_results),
        }
        # Initiative 1.3: Token Compression
        self.logger.info("-" * 80)
        self.logger.info("INITIATIVE 1.3: TOKEN COMPRESSION")
        self.logger.info("-" * 80)
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

        total_before = 0
        total_after = 0

        for _name, prompt in test_prompts:
            analysis = optimizer.analyzePrompt(prompt, "test-agent")
            total_before += analysis["tokensBefore"]
            total_after += analysis["tokensAfter"]

        overall_compression = (
            (total_before - total_after) / total_before * 100 if total_before > 0 else 0
        )

        token_result = {
            "total_before": total_before,
            "total_after": total_after,
            "compression_percent": round(overall_compression, 1),
            "pass": overall_compression >= 25,
        }

        results["initiatives"]["token"] = token_result

        self.logger.info(f"Compression: {overall_compression:.1f}%")
        self.logger.info(f"Target: >=25% | Status: {'PASS' if token_result['pass'] else 'FAIL'}")

        # Initiative 1.4: Concurrency Scaling
        self.logger.info("-" * 80)
        self.logger.info("INITIATIVE 1.4: CONCURRENCY SCALING")
        self.logger.info("-" * 80)

        scaling_results = []
        baseline_throughput = 0

        for load_count in [50, 100, 150]:
            tasks = []
            for i in range(load_count):
                task = processor.createBatchTask(
                    taskId=f"gate-conc-{load_count}-{i}",
                    agentId="test",
                    description=f"Concurrent task {i}",
                )
            tasks.append(task)

            start = time.perf_counter()
            processor.processBatchesPipelined(tasks)
            elapsed = time.perf_counter() - start

            throughput = load_count / elapsed if elapsed > 0 else 0

            if load_count == 50:
                baseline_throughput = throughput

            scaling = throughput / baseline_throughput if baseline_throughput > 0 else 1.0

            # Scaling targets: >=1.8x at 2x load (100 tasks), >=2.5x at 3x load (150 tasks)
            if load_count == 100:
                expected = 1.8
            elif load_count == 150:
                expected = 2.5
            else:
                expected = 1.0

            pass_scaling = scaling >= expected
            scaling_results.append(
                {
                    "load": load_count,
                    "throughput": round(throughput, 2),
                    "scaling": round(scaling, 2),
                    "expected": expected,
                    "pass": pass_scaling,
                }
            )

            self.logger.info(
                f"Load {load_count:3d}: {scaling:.2f}x scaling (target {expected:.1f}x) - {'PASS' if pass_scaling else 'FAIL'}"
            )

        results["initiatives"]["concurrency"] = {
            "results": scaling_results,
            "aggregate_pass": all(r["pass"] for r in scaling_results),
        }

        # Gate Closure Criteria Summary
        self.logger.info("=" * 80)
        self.logger.info("GATE CLOSURE CRITERIA SUMMARY")
        self.logger.info("=" * 80)

        criteria = {
            "routing_latency": routing_result["pass"],
            "batch_throughput": results["initiatives"]["batch"]["aggregate_pass"],
            "token_compression": token_result["pass"],
            "concurrency_scaling": results["initiatives"]["concurrency"]["aggregate_pass"],
        }

        results["gate_closure_criteria"] = criteria

        all_pass = all(criteria.values())
        results["overall_status"] = "PASS" if all_pass else "FAIL"

        for criterion, status in criteria.items():
            status_str = "PASS" if status else "FAIL"
            self.logger.info(f"{criterion:30s}: {status_str}")

        self.logger.info("=" * 80)
        self.logger.info(f"PHASE 17 GATE CLOSURE: {results['overall_status']}")
        self.logger.info("=" * 80)

        return results

    def generateReport(self, results: Dict[str, Any]) -> str:
        """Generate gate closure report."""
        if results["overall_status"] == "PASS":
            report = """
PHASE 17 GATE CLOSURE APPROVED

All 4 initiatives verified and ready for production.
Optimization targets all exceeded.

Next Steps:
   1. Week 5-6: Final documentation and handoff
2. Operations team sign-off
3. Phase 17 official closure: Friday 10/3
4. Begin planning for next optimization phase
"""
        else:
            report = """
PHASE 17 GATE CLOSURE PENDING

Some criteria not yet met. Review results and remediate.
"""
        return report


def main() -> int:
    """Run gate closure validation."""
    import asyncio

    validator = GateClosureValidator()
    results = asyncio.run(validator.validateAllInitiatives())
    # Save results using BaseProfiler
    validator.saveMetrics("results", results)
    # Generate and save report
    report = validator.generateReport(results)
    validator.saveReport("gate_closure_report", report)
    validator.logger.info("Gate closure validation complete.")


if __name__ == "__main__":
    main()
