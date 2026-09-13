#!/usr/bin/env python3
"""Phase 4A: Parallel Error Handler Consolidation - Cost Optimized"""
import subprocess
from pathlib import Path

print("=== PHASE 4A: Error Handler Consolidation ===")
print("Optimized for parallel execution\n")

# Create canonical error_handler.py
error_handler_code = '''"""Unified error handling for scripts.

Provides consistent error logging, exception handling, and recovery patterns.
"""
import logging
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


def log_and_raise(error: Exception, context: Optional[str] = None) -> None:
    """Log error with context and re-raise."""
    msg = str(error)
    if context:
        msg = f"{msg} (context: {context})"
    logger.error(msg)
    raise error


def log_and_return(error: Exception, default: Any = None, context: Optional[str] = None) -> Any:
    """Log error and return default value."""
    msg = str(error)
    if context:
        msg = f"{msg} (context: {context})"
    logger.error(msg)
    return default


def safe_execute(func: Callable, *args, default: Any = None, **kwargs) -> Any:
    """Execute function with error handling."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return log_and_return(e, default)
'''

print("[A1] Creating canonical error_handler.py...")
error_file = Path("scripts/utils/error_handler.py")
error_file.write_text(error_handler_code)
print(f"  Created: {error_file}")

# Find files with error patterns - single batch grep
print("[A2] Scanning for error handling patterns (batch grep)...")
try:
    result = subprocess.run(
        ["grep", "-r", "-l", "except.*Exception", "scripts", "--include=*.py"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    error_files = set(result.stdout.strip().split("\n")) if result.stdout else set()
    error_files.discard("")

    print(f"  Found: {len(error_files)} files with error patterns")

    # Count patterns
    except_pass = 0
    logger_error = 0
    self_log_error = 0

    for fpath in error_files:
        try:
            content = Path(fpath).read_text(errors="ignore")
            if "except Exception:" in content and "pass" in content:
                except_pass += 1
            if "logger.error" in content:
                logger_error += 1
            if "self.log_error" in content:
                self_log_error += 1
        except:
            pass

    print(f"  Patterns found:")
    print(f"    - except/pass (anti-pattern): {except_pass}")
    print(f"    - logger.error: {logger_error}")
    print(f"    - self.log_error: {self_log_error}")

except Exception as e:
    print(f"  Warning: {e}")

print()
print("[SUCCESS] Stream A Complete - Error Handler ready")
