#!/usr/bin/env python3
"""
Parametrization Performance Measurement & Metrics Collection

Measures execution time, memory usage, and coverage metrics for parametrized tests.
Generates baseline reports and detects performance regressions.

Usage:
    python scripts/measure_parametrization_perf.py [--baseline] [--compare] [--report]

Options:
    --baseline    Generate baseline metrics (saves to data/)
    --compare     Compare against baseline, report regressions
    --report      Generate detailed report
"""

import json
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)



class ParametrizationMetrics:
    """Collect and analyze parametrized test metrics."""

    def __init__(self, output_dir: str = "parametrization-metrics"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.baseline_dir = Path("parametrization-baseline")
        self.baseline_dir.mkdir(exist_ok=True)

    def collect_test_information(self) -> Dict[str, Any]:
        """Collect information about all tests and parametrized tests."""
        logger.info("Collecting test information...")

        result = subprocess.run(
            ["pytest", "tests/", "--collect-only", "-q"],
            capture_output=True,
            text=True,
        )

        output_lines = result.stdout.strip().split("\n")
        total_tests = len([l for l in output_lines if l.startswith("tests/")])

        # Count parametrized tests
        result = subprocess.run(
            ["grep", "-r", "@pytest.mark.parametrize", "tests/", "--include=*.py"],
            capture_output=True,
            text=True,
        )

        parametrized_count = len([l for l in result.stdout.split("\n") if l.strip()])

        # Count parametrized test functions
        result = subprocess.run(
            [
                "grep",
                "-r",
                "@pytest.mark.parametrize",
                "tests/",
                "--include=*.py",
                "-A1",
            ],
            capture_output=True,
            text=True,
        )

        functions = [l for l in result.stdout.split("\n") if "def test" in l]

        return {
            "total_tests": total_tests,
            "parametrized_decorators": parametrized_count,
            "parametrized_functions": len(functions),
            "adoption_rate": (len(functions) / total_tests * 100 if total_tests > 0 else 0),
            "collected_at": datetime.now().isoformat(),
        }

    def run_tests_with_timing(self) -> Dict[str, Any]:
        """Run tests and measure execution time."""
        logger.info("Running tests with performance measurement...")

        start_time = time.time()

        result = subprocess.run(
            [
                "pytest",
                "tests/",
                "-v",
                "--tb=short",
                "--json-report",
                f"--json-report-file={self.output_dir}/test-report.json",
                "--benchmark-only",
                f"--benchmark-json={self.output_dir}/benchmark-results.json",
                "-m",
                "not slow",
            ],
            capture_output=True,
            text=True,
        )

        elapsed = time.time() - start_time

        # Parse test report
        try:
            with open(self.output_dir / "test-report.json") as f:
                report = json.load(f)

            summary = report.get("summary", {})

            return {
                "total_tests": summary.get("total", 0),
                "passed": summary.get("passed", 0),
                "failed": summary.get("failed", 0),
                "skipped": summary.get("skipped", 0),
                "pass_rate": (
                    summary.get("passed", 0) / summary.get("total", 1) * 100
                    if summary.get("total", 0) > 0
                    else 0
                ),
                "execution_time_seconds": elapsed,
                "status": "passed" if result.returncode == 0 else "failed",
            }
        except Exception as e:
            logger.info(f"Warning: Could not parse test report: {e}")
            return {
                "execution_time_seconds": elapsed,
                "status": "error",
                "error": str(e),
            }

    def parse_benchmark_results(self) -> Dict[str, Any]:
        """Parse benchmark results."""
        try:
            with open(self.output_dir / "benchmark-results.json") as f:
                benchmarks = json.load(f)

            if not benchmarks.get("benchmarks"):
                return {"note": "No benchmarks available"}

            times = [b["stats"]["mean"] for b in benchmarks["benchmarks"]]
            return {
                "benchmark_count": len(benchmarks["benchmarks"]),
                "average_time_seconds": sum(times) / len(times),
                "min_time_seconds": min(times),
                "max_time_seconds": max(times),
                "total_time_seconds": sum(times),
            }
        except Exception as e:
            logger.info(f"Note: Benchmark analysis skipped ({e})")
            return {}

    def load_baseline(self) -> Dict[str, Any]:
        """Load baseline metrics for comparison."""
        try:
            with open(self.baseline_dir / "baseline-metrics.json") as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def compare_against_baseline(
        """Compare_against_baseline operation."""
        self, current: Dict[str, Any], baseline: Dict[str, Any]
    ) -> Dict[str, Any]:
    """Compare parametrization performance against baseline."""
        """Compare current metrics against baseline."""
        if not baseline:
            return {"note": "No baseline available"}

        regressions = []
        improvements = []

        # Check test count
        if current.get("total_tests", 0) > baseline.get("total_tests", 0):
            improvements.append(
                f"Test count increased from {baseline['total_tests']} to {current['total_tests']}"
            )

        # Check pass rate
        if current.get("pass_rate", 0) < baseline.get("pass_rate", 100):
            regressions.append(
                f"Pass rate decreased from {baseline['pass_rate']:.1f}% to {current['pass_rate']:.1f}%"
            )

        # Check execution time
        current_time = current.get("execution_time_seconds", 0)
        baseline_time = baseline.get("execution_time_seconds", 0)
        if baseline_time > 0:
            time_increase = (current_time / baseline_time - 1) * 100
            if time_increase > 10:  # 10% increase threshold
                regressions.append(
                    f"Execution time increased by {time_increase:.1f}% ({baseline_time:.2f}s → {current_time:.2f}s)"
                )
            elif time_increase < -10:
                improvements.append(
                    f"Execution time improved by {-time_increase:.1f}% ({baseline_time:.2f}s → {current_time:.2f}s)"
                )

        return {
            "regressions": regressions,
            "improvements": improvements,
            "status": "regression_detected" if regressions else "healthy",
        }

    def generate_report(self, metrics: Dict[str, Any]) -> str:
        """Generate human-readable report."""
        report = []
        report.append("# Parametrization Metrics Report")
        report.append("")
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append("")

        report.append("## Test Collection Metrics")
        if "total_tests" in metrics and isinstance(metrics.get("test_info"), dict):
            info = metrics["test_info"]
            report.append(f"- Total Tests: {info.get('total_tests', 'N/A')}")
            report.append(f"- Parametrized Functions: {info.get('parametrized_functions', 'N/A')}")
            report.append(f"- Adoption Rate: {info.get('adoption_rate', 0):.1f}%")

        report.append("")
        report.append("## Execution Metrics")
        if "execution" in metrics:
            exec_metrics = metrics["execution"]
            report.append(f"- Total Tests Run: {exec_metrics.get('total_tests', 'N/A')}")
            report.append(f"- Passed: {exec_metrics.get('passed', 'N/A')}")
            report.append(f"- Failed: {exec_metrics.get('failed', 'N/A')}")
            report.append(f"- Pass Rate: {exec_metrics.get('pass_rate', 0):.1f}%")
            report.append(f"- Execution Time: {exec_metrics.get('execution_time_seconds', 0):.2f}s")

        if "benchmark" in metrics:
            report.append("")
            report.append("## Performance Metrics")
            bench = metrics["benchmark"]
            if "average_time_seconds" in bench:
                report.append(f"- Average Test Time: {bench['average_time_seconds']:.3f}s")
                report.append(f"- Min Time: {bench['min_time_seconds']:.3f}s")
                report.append(f"- Max Time: {bench['max_time_seconds']:.3f}s")

        if "comparison" in metrics and metrics["comparison"].get("regressions"):
            report.append("")
            report.append("## ⚠️ Regressions Detected")
            for regression in metrics["comparison"]["regressions"]:
                report.append(f"- {regression}")

        if "comparison" in metrics and metrics["comparison"].get("improvements"):
            report.append("")
            report.append("## ✅ Improvements")
            for improvement in metrics["comparison"]["improvements"]:
                report.append(f"- {improvement}")

        return "\n".join(report)

    def save_metrics(self, metrics: Dict[str, Any], filename: str = "metrics.json") -> None:
        """Save metrics to JSON file."""
        filepath = self.output_dir / filename
        with open(filepath, "w") as f:
            json.dump(metrics, f, indent=2)
        logger.info(f"Metrics saved to {filepath}")

    def save_baseline(self, metrics: Dict[str, Any]) -> None:
        """Save baseline metrics."""
        baseline_file = self.baseline_dir / "baseline-metrics.json"
        with open(baseline_file, "w") as f:
            json.dump(metrics, f, indent=2)
        logger.info(f"Baseline saved to {baseline_file}")

    def run(self, args: List[str] = None) -> int:
        """Run metrics collection."""
        args = args or sys.argv[1:]

        logger.info("=" * 60)
        logger.info("Parametrization Performance Metrics")
        logger.info("=" * 60)
        logger.info()

        # Collect metrics
        test_info = self.collect_test_information()
        execution_metrics = self.run_tests_with_timing()
        benchmark_metrics = self.parse_benchmark_results()

        all_metrics = {
            "test_info": test_info,
            "execution": execution_metrics,
            "benchmark": benchmark_metrics,
        }

        # Compare against baseline if available
        baseline = self.load_baseline()
        if baseline and "--compare" in args:
            comparison = self.compare_against_baseline(execution_metrics, baseline)
            all_metrics["comparison"] = comparison

            logger.info("\nComparison Results:")
            for item in comparison.get("regressions", []):
                logger.info(f"  ⚠️  {item}")
            for item in comparison.get("improvements", []):
                logger.info(f"  ✅ {item}")

        # Generate and print report
        report = self.generate_report(all_metrics)
        logger.info("\n" + report)

        # Save metrics
        self.save_metrics(all_metrics)

        # Save as baseline if requested
        if "--baseline" in args:
            self.save_baseline(execution_metrics)

        logger.info()
        logger.info("=" * 60)
        logger.info("✅ Metrics collection complete")
        logger.info(f"Output: {self.output_dir}/")
        logger.info("=" * 60)

        return 0


if __name__ == "__main__":
    collector = ParametrizationMetrics()
    sys.exit(collector.run())
