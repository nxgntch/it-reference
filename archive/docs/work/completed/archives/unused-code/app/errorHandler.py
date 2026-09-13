"""Unified exception handling utilities for consistent error handling patterns.

Consolidates try-except-log-return patterns used across modules to eliminate
duplicated error handling code.
"""

import functools
import logging
from contextlib import contextmanager
from typing import Any, Callable, Optional, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


def safelyCall(
    operation: Callable[..., T],
    operationName: str = "",
    defaultReturn: Any = None,
    logLevel: str = "error",
    reraise: bool = False,
) -> T:
    """Execute operation with exception handling and logging.

    Args:
        operation: Callable to execute
        operationName: Description of the operation (for logging)
        defaultReturn: Value to return if exception occurs
        logLevel: Logging level ("error", "warning", "info", "debug")
        reraise: If True, re-raise exception after logging

    Returns:
        Result of operation or defaultReturn if exception occurs

    Raises:
        Original exception if reraise=True
    """
    try:
        return operation()
    except Exception as e:
        logFunc = getattr(logger, logLevel, logger.error)
        logFunc(f"{operationName or 'Operation'} failed: {e}")
        if reraise:
            raise
        return defaultReturn


def safely(
    *,
    operationName: str = "",
    defaultReturn: Any = None,
    logLevel: str = "error",
    reraise: bool = False,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for safe exception handling with logging.

    Usage:
        @safely(operationName="load config", defaultReturn={})
        def loadConfig():
            return yaml.safe_load(...)

    Args:
        operationName: Description of operation (for logging)
        defaultReturn: Value to return on exception
        logLevel: Logging level ("error", "warning", "info", "debug")
        reraise: If True, re-raise exception after logging

    Returns:
        Decorator function
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logFunc = getattr(logger, logLevel, logger.error)
                desc = operationName or f"{func.__name__}"
                logFunc(f"{desc} failed: {e}")
                if reraise:
                    raise
                return defaultReturn

        return wrapper

    return decorator


@contextmanager
def safeContext(
    operationName: str = "",
    logLevel: str = "error",
    reraise: bool = False,
    onError: Optional[Callable[[Exception], None]] = None,
):
    """Context manager for safe exception handling.

    Usage:
        with safeContext("database query", logLevel="warning"):
            result = execute_query()

    Args:
        operationName: Description of operation (for logging)
        logLevel: Logging level ("error", "warning", "info", "debug")
        reraise: If True, re-raise exception after logging
        onError: Optional callback invoked with exception

    Yields:
        None (exception caught and logged within context)

    Raises:
        Original exception if reraise=True
    """
    try:
        yield
    except Exception as e:
        logFunc = getattr(logger, logLevel, logger.error)
        logFunc(f"{operationName or 'Operation'} failed: {e}")

        if onError:
            onError(e)

        if reraise:
            raise


def safelyDict(
    operation: Callable[..., dict],
    operationName: str = "",
    logLevel: str = "error",
) -> dict:
    """Execute operation and return dict, with error fallback to empty dict.

    Args:
        operation: Callable returning dict
        operationName: Description of operation (for logging)
        logLevel: Logging level ("error", "warning", "info", "debug")

    Returns:
        Result dict or empty dict on exception
    """
    return safelyCall(operation, operationName, {}, logLevel)


def safelyList(
    operation: Callable[..., list],
    operationName: str = "",
    logLevel: str = "error",
) -> list:
    """Execute operation and return list, with error fallback to empty list.

    Args:
        operation: Callable returning list
        operationName: Description of operation (for logging)
        logLevel: Logging level ("error", "warning", "info", "debug")

    Returns:
        Result list or empty list on exception
    """
    return safelyCall(operation, operationName, [], logLevel)


def safelyBool(
    operation: Callable[..., bool],
    operationName: str = "",
    defaultValue: bool = False,
    logLevel: str = "error",
) -> bool:
    """Execute operation and return bool, with error fallback.

    Args:
        operation: Callable returning bool
        operationName: Description of operation (for logging)
        defaultValue: Default bool value on exception
        logLevel: Logging level ("error", "warning", "info", "debug")

    Returns:
        Result bool or defaultValue on exception
    """
    return safelyCall(operation, operationName, defaultValue, logLevel)
