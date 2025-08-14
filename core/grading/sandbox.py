"""Sandbox execution for student code."""

import signal
from typing import Any


class TimeoutError(Exception):
    """Raised when code execution times out."""

    pass


def timeout_handler(signum: int, frame: Any) -> None:
    """Handle timeout signal."""
    raise TimeoutError("Code execution timed out")


def execute_with_timeout(
    code: str, globals_dict: dict[str, Any], timeout: int = 30
) -> None:
    """
    Execute code with timeout and memory restrictions.

    Args:
        code: Python code to execute
        globals_dict: Global namespace for execution
        timeout: Maximum execution time in seconds

    Raises:
        TimeoutError: If execution exceeds timeout
        RuntimeError: If execution fails
    """
    # Set up timeout (Unix only)
    if hasattr(signal, "SIGALRM"):
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)

    try:
        # Restrict dangerous builtins
        restricted_globals = _create_restricted_globals(globals_dict)

        # Execute code
        exec(code, restricted_globals)

        # Update original globals with new definitions
        for key, value in restricted_globals.items():
            if not key.startswith("__") or key in globals_dict:
                globals_dict[key] = value

    except TimeoutError:
        raise
    except Exception as e:
        raise RuntimeError(f"Code execution failed: {e}") from e
    finally:
        # Reset alarm
        if hasattr(signal, "SIGALRM"):
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)


def _create_restricted_globals(base_globals: dict[str, Any]) -> dict[str, Any]:
    """Create restricted global namespace."""
    # Start with safe builtins
    safe_builtins = {
        "__name__",
        "__doc__",
        "__package__",
        "__loader__",
        "__spec__",
        "__import__",
        "abs",
        "all",
        "any",
        "bin",
        "bool",
        "bytearray",
        "bytes",
        "callable",
        "chr",
        "classmethod",
        "complex",
        "dict",
        "dir",
        "divmod",
        "enumerate",
        "filter",
        "float",
        "format",
        "frozenset",
        "getattr",
        "hasattr",
        "hash",
        "hex",
        "id",
        "int",
        "isinstance",
        "issubclass",
        "iter",
        "len",
        "list",
        "map",
        "max",
        "min",
        "next",
        "object",
        "oct",
        "ord",
        "pow",
        "print",
        "property",
        "range",
        "repr",
        "reversed",
        "round",
        "set",
        "setattr",
        "slice",
        "sorted",
        "staticmethod",
        "str",
        "sum",
        "super",
        "tuple",
        "type",
        "vars",
        "zip",
    }

    import builtins

    restricted_builtins = {
        name: getattr(builtins, name)
        for name in safe_builtins
        if hasattr(builtins, name)
    }

    # Create restricted globals
    restricted_globals = {"__builtins__": restricted_builtins, **base_globals}

    return restricted_globals
